from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .. import schemas, crud
from ..database import get_db
from ..config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

# For simplicity, a basic token validation. In a real app, use JWTs with proper signing.
async def verify_admin_token(token: str = Depends(oauth2_scheme)):
    if token != settings.ADMIN_PASSWORD: # Using ADMIN_PASSWORD as a simple token for now
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")
    return token

@router.post("/admin/login")
async def admin_login(password: str = Body(..., embed=True)):
    if password == settings.ADMIN_PASSWORD:
        # In a real app, generate a JWT here
        return {"access_token": settings.ADMIN_PASSWORD, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

@router.get("/admin/list", response_model=List[schemas.WaitlistOut])
async def admin_list_waitlist_entries(
    token: str = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
    email: Optional[str] = Query(None),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    entries = await crud.get_waitlist_entries(
        db,
        email=email,
        first_name=first_name,
        last_name=last_name,
        country=country,
        search=search
    )
    return entries
