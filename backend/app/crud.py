from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import Optional

from . import models, schemas

async def create_waitlist_entry(db: AsyncSession, entry: schemas.WaitlistCreate, country: Optional[str] = None):
    db_entry = models.Waitlist(
        email=entry.email.lower().strip(),
        first_name=entry.first_name,
        last_name=entry.last_name,
        country=country
    )
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

async def get_waitlist_entry_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.Waitlist).filter(models.Waitlist.email == email.lower().strip()))
    return result.scalar_one_or_none()

async def get_waitlist_entries(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    country: Optional[str] = None,
    search: Optional[str] = None
):
    query = select(models.Waitlist)

    if email:
        query = query.filter(models.Waitlist.email.ilike(f"%{email.lower().strip()}%" ))
    if first_name:
        query = query.filter(models.Waitlist.first_name.ilike(f"%{first_name.strip()}%" ))
    if last_name:
        query = query.filter(models.Waitlist.last_name.ilike(f"%{last_name.strip()}%" ))
    if country:
        query = query.filter(models.Waitlist.country.ilike(f"%{country.strip()}%" ))

    if search:
        search_pattern = f"%{search.lower().strip()}%"
        query = query.filter(
            or_(
                models.Waitlist.email.ilike(search_pattern),
                models.Waitlist.first_name.ilike(search_pattern),
                models.Waitlist.last_name.ilike(search_pattern),
                models.Waitlist.country.ilike(search_pattern),
            )
        )

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()
