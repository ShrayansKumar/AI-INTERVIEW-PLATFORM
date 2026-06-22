import asyncio
from app.db.session import AsyncSessionLocal
from app.models.admin import Admin
from app.core.security import hash_password


async def create_admin():
    async with AsyncSessionLocal() as db:
        admin = Admin(username="admin", password=hash_password("changeme123"))
        db.add(admin)
        await db.commit()
        print("Admin created: username=admin")


if __name__ == "__main__":
    asyncio.run(create_admin())