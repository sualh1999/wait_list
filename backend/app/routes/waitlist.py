from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .. import schemas, crud
from ..database import get_db
from ..utils.email import send_welcome_email
from ..utils.geo import get_country_from_ip

router = APIRouter()

@router.post("/waitlist", response_model=schemas.WaitlistOut, status_code=status.HTTP_201_CREATED)
async def create_waitlist_entry(request: Request, entry: schemas.WaitlistCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    # Normalize email
    normalized_email = entry.email.lower().strip()

    # Check for duplicate email
    db_entry = await crud.get_waitlist_entry_by_email(db, normalized_email)
    if db_entry:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already on waitlist")

    # Get client IP and detect country
    client_ip = request.headers.get("x-forwarded-for")
    if client_ip:
        # Sometimes multiple IPs are listed, take the first
        client_ip = client_ip.split(",")[0].strip()
    else:
        # fallback to request.client.host (usually internal)
        client_ip = request.client.host if request.client else None
    country = await get_country_from_ip(client_ip)

    try:
        new_entry = await crud.create_waitlist_entry(db, entry, country)
        background_tasks.add_task(send_welcome_email, new_entry.email)
        return new_entry
    except IntegrityError:
        # This catches a race condition if two requests try to insert the same email simultaneously
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already on waitlist")
