from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .. import schemas, crud
from ..database import get_db
from ..utils.email import send_welcome_email

router = APIRouter()

@router.post("/waitlist", response_model=schemas.WaitlistOut, status_code=status.HTTP_201_CREATED)
async def create_waitlist_entry(entry: schemas.WaitlistCreate, db: AsyncSession = Depends(get_db)):
    # Normalize email
    normalized_email = entry.email.lower().strip()

    # Check for duplicate email
    db_entry = await crud.get_waitlist_entry_by_email(db, normalized_email)
    if db_entry:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already on waitlist")

    try:
        new_entry = await crud.create_waitlist_entry(db, schemas.WaitlistCreate(email=normalized_email))
        await send_welcome_email(new_entry.email)
        return new_entry
    except IntegrityError:
        # This catches a race condition if two requests try to insert the same email simultaneously
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already on waitlist")
