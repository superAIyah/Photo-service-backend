from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager

from database import get_async_session

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()


@router.get("/albums")
async def get_albums(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return "Your albums ..."

@router.post("/add_album")
async def add_album(
        name: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return "You added album ..."

@router.post("/remove_album")
async def remove_album(
        id_album: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return "You removed album ..."


@router.get("/photoes")
async def get_photoes(
        id_album: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return "Your photoes by album id ..."

@router.post("/add_photo")
async def add_photo(
        id_album: int,
        name: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return "You added album ..."

@router.post("/add_photo")
async def remove_photo(
        id_album: int,
        id_photo: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return "You added album ..."


