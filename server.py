from fastapi import FastAPI, APIRouter, Depends, File, UploadFile
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from typing import Annotated

from auth.database import get_async_session
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from auth.database import User
from auth.database import InsertAlbum, InsertPhoto
from models.models import album, photo
from PIL import Image
import io
import sys
import uuid

sys.path.insert(0, './proto')
from proto.grpc_client import grpc_client

client = grpc_client()  # gRPC S3-backend client

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()
app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


async def get_album_id(uuid_album: str, session: AsyncSession) -> int:
    query = select(album).where(album.c.uuid == uuid_album)
    result = await session.execute(query)
    return result.mappings().all()[0]["id"]


async def get_photo_id(uuid_photo: str, session: AsyncSession) -> int:
    query = select(photo).where(photo.c.uuid == uuid_photo)
    result = await session.execute(query)
    return result.mappings().all()[0]["id"]


@app.get("/")
async def root():
    return 'Photo service backend by @FedorX8'


@router.get("/albums")
async def get_albums(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    query = select(album).where(album.c.id_user == user.id)
    result = await session.execute(query)
    return result.mappings().all()


@router.post("/add_album")
async def add_album(
        name: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    uuid_album = str(uuid.uuid4())
    album_insert = InsertAlbum(user.id, name, uuid_album)
    stmt = insert(album).values(album_insert.__dict__)
    await session.execute(stmt)
    await session.commit()

    id_album = await get_album_id(uuid_album, session)
    return {"status": "success", "uuid_album": uuid_album, "id_album": id_album}


@router.post("/remove_album")
async def remove_album(
        uuid_album: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    query = select(album).where(album.c.uuid == uuid_album)
    result = await session.execute(query)
    albs = result.mappings().all()
    if not len(albs):
        return {"status": "not in base"}
    id_album = await get_album_id(uuid_album, session)

    query = select(photo).where(photo.c.id_album == id_album)
    get_result = await session.execute(query)
    for elem in get_result.mappings().all():
        await remove_photo(elem.uuid, session, user)

    stmt = delete(album).where(album.c.id == id_album)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/photoes")
async def get_photoes(
        uuid_album: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    id_album = await get_album_id(uuid_album, session)
    query = select(photo).where(photo.c.id_album == id_album)
    result = await session.execute(query)
    return result.mappings().all()


@router.post("/add_photo")
async def add_photo(
        uuid_album: str,
        name: str,
        img: Annotated[bytes, File()],
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    id_album = await get_album_id(uuid_album, session)
    uuid_photo = str(uuid.uuid4())
    result = client.add_photo_request(uuid_photo, img)
    url = result.url
    photo_insert = InsertPhoto(user.id, id_album, uuid_photo, name, url)
    stmt = insert(photo).values(photo_insert.__dict__)
    await session.execute(stmt)
    await session.commit()

    id_photo = await get_photo_id(uuid_photo, session)
    return {"status": "success", "url": url, "uuid_photo": uuid_photo, "id_photo": id_photo}

@router.post("/remove_photo")
async def remove_photo(
        uuid_photo: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    client.remove_photo_request(uuid_photo)
    query = select(photo).where(photo.c.uuid == uuid_photo)
    result = await session.execute(query)
    if not len(result.mappings().all()):
        return {"status": "not in base"}
    stmt = delete(photo).where(photo.c.uuid == uuid_photo)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


app.include_router(router)


@app.get("/protected-route")
def protected_route(album_name: str, user: User = Depends(current_user)):
    return f"Hello, {user.email}, id = {user.id}"
