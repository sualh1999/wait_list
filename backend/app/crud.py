from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, schemas

async def create_waitlist_entry(db: AsyncSession, entry: schemas.WaitlistCreate):
    db_entry = models.Waitlist(email=entry.email.lower().strip())
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

async def get_waitlist_entry_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.Waitlist).filter(models.Waitlist.email == email.lower().strip()))
    return result.scalar_one_or_none()

async def get_waitlist_entries(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Waitlist).offset(skip).limit(limit))
    return result.scalars().all()
