import asyncio
import random
import json
import os
from faker import Faker
from tqdm import tqdm
import httpx

BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "adminpass"

TOTAL_ITEMS = 100_000
CONCURRENCY = 10
CHECKPOINT_FILE = "item_checkpoint.json"

fake = Faker()

# ---------------- AUTH ----------------
async def get_token():
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{BASE_URL}/auth/token",
            data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
        )
        r.raise_for_status()
        return r.json()["access_token"]

# ---------------- CHECKPOINT ----------------
def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)["last_index"]
    return 0

def save_checkpoint(i):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_index": i}, f)

# ---------------- FETCH USER IDS ----------------
async def fetch_all_user_ids(token):
    headers = {"Authorization": f"Bearer {token}"}
    user_ids = []

    async with httpx.AsyncClient(timeout=60) as client:
        skip = 0
        limit = 200

        while True:
            r = await client.get(
                f"{BASE_URL}/users/",
                params={"skip": skip, "limit": limit},
                headers=headers,
            )
            r.raise_for_status()

            users = r.json()
            if not users:
                break

            user_ids.extend(u["id"] for u in users)
            skip += limit

    print(f"✅ Loaded {len(user_ids)} users")
    return user_ids

# ---------------- CREATE ITEM ----------------
async def create_item(client, token, owner_id, retries=5):
    payload = {
        "title": fake.word().title(),
        "description": fake.sentence(),
        "price": round(random.uniform(100, 5000), 2),
    }
    headers = {"Authorization": f"Bearer {token}"}

    for attempt in range(retries):
        try:
            r = await client.post(
                f"{BASE_URL}/items/",
                json=payload,
                headers=headers,
            )

            if r.status_code in (400, 409):
                return

            r.raise_for_status()
            return

        except (httpx.ReadTimeout, httpx.ConnectError):
            await asyncio.sleep(2 ** attempt)

    print("❌ Item creation failed permanently")

# ---------------- SEED ITEMS ----------------
async def seed_items(token):
    start = load_checkpoint()
    print(f"▶ Resuming from item index: {start}")

    user_ids = await fetch_all_user_ids(token)

    limits = httpx.Limits(
        max_connections=CONCURRENCY,
        max_keepalive_connections=CONCURRENCY,
    )

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(60),
        limits=limits,
    ) as client:

        tasks = []
        for i in tqdm(range(start, TOTAL_ITEMS), initial=start, total=TOTAL_ITEMS):
            owner_id = random.choice(user_ids)
            tasks.append(create_item(client, token, owner_id))

            if len(tasks) >= CONCURRENCY:
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks.clear()
                save_checkpoint(i)

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

# ---------------- MAIN ----------------
async def main():
    print("🔐 Fetching token...")
    token = await get_token()

    print("📦 Seeding items...")
    await seed_items(token)

    print("✅ Item seeding completed")

if __name__ == "__main__":
    asyncio.run(main())
