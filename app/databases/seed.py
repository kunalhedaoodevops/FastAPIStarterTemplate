from sqlalchemy.orm import Session
from ..models.users import User
from ..utils import security
from ..databases.db import get_db

def run_seed(db: Session = next(get_db())):
    try:
        # ---- admin user ----
        admin_email = "admin@example.com"

        admin = db.query(User).filter(User.email == admin_email).first()

        if not admin:
            admin = User(
                email=admin_email,
                full_name="Admin",
                hashed_password=security.get_password_hash("adminpass"),  # 🔒 hash in real apps
                role="admin",
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print("✅ Admin user created")
        else:
            print("ℹ️ Admin user already exists")

        # ---- optional default user ----
        user_email = "user@example.com"
        user = db.query(User).filter(User.email == user_email).first()

        if not user:
            user = User(
                email=user_email,
                full_name="User",
                hashed_password=security.get_password_hash("adminpass"),
                role="user",
                is_active=True,
            )
            db.add(user)
            db.commit()
            print("✅ Default user created")

    except Exception as e:
        db.rollback()
        print("❌ Seeding failed:", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
