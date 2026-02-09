import asyncio
import random
from faker import Faker
from tqdm import tqdm
import httpx
import json
import os

BASE_URL = "http://127.0.0.1:8000"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "adminpass"

TOTAL_USERS = 100_000
CONCURRENCY = 10
CHECKPOINT_FILE = "user_checkpoint.json"

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

# ---------------- USER CREATION ----------------
async def create_user(client, token, i, retries=5):
    payload = {
        "email": f"user{i}@example.com",
        "password": "password123",
        "full_name": fake.name(),
        "role": "user",
    }
    headers = {"Authorization": f"Bearer {token}"}

    for attempt in range(retries):
        try:
            r = await client.post(
                f"{BASE_URL}/users/",
                json=payload,
                headers=headers,
            )

            # duplicate user → safe skip
            if r.status_code in (400, 409):
                return

            r.raise_for_status()
            return

        except (httpx.ReadTimeout, httpx.ConnectError):
            await asyncio.sleep(2 ** attempt)

    print(f"❌ Failed permanently: user{i}")

async def seed_users(token):
    start = load_checkpoint()
    print(f"▶ Resuming from user index: {start}")

    limits = httpx.Limits(
        max_connections=CONCURRENCY,
        max_keepalive_connections=CONCURRENCY,
    )

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(60),
        limits=limits,
    ) as client:

        tasks = []
        for i in tqdm(range(start, TOTAL_USERS), initial=start, total=TOTAL_USERS):
            tasks.append(create_user(client, token, i))

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

    print("👤 Seeding users...")
    await seed_users(token)

    print("✅ User seeding completed")

if __name__ == "__main__":
    asyncio.run(main())
