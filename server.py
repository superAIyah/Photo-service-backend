from fastapi import FastAPI, APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete

from auth.database import get_async_session
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from auth.database import User
from auth.database import InsertAlbum, InsertPhoto
from models.models import album, photo
from PIL import Image
import io
import pathlib
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


# @app.get("/")
# async def test():
#     response = client.get_photo_request(uuid='pepe.png')
#     print(response)
#     return 'test'

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
    album_insert = InsertAlbum(user.id, name, str(uuid.uuid4()))
    stmt = insert(album).values(album_insert.__dict__)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.post("/remove_album")
async def remove_album(
        id_album: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    query = select(album).where(album.c.id == id_album)
    result = await session.execute(query)
    if not len(result.mappings().all()):
        return {"status": "not in base"}

    query = select(photo).where(photo.c.id_album == id_album)
    get_result = await session.execute(query)
    for elem in get_result.mappings().all():
        await remove_photo(elem.id, session, user)

    stmt = delete(album).where(album.c.id == id_album)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/photoes")
async def get_photoes(
        id_album: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    query = select(photo).where(photo.c.id_album == id_album)
    result = await session.execute(query)
    return result.mappings().all()


@router.post("/add_photo")
async def add_photo(
        id_album: int,
        name: str,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    img = Image.open("cot.jpeg", mode='r')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    uid = str(uuid.uuid4())
    result = client.add_photo_request(uid, img_byte_arr)
    url = result.url
    photo_insert = InsertPhoto(user.id, id_album, uid, url)
    stmt = insert(photo).values(photo_insert.__dict__)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.post("/remove_photo")
async def remove_photo(
        id_photo: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    query = select(photo).where(photo.c.id == id_photo)
    result = await session.execute(query)
    if not len(result.mappings().all()):
        return {"status": "not in base"}
    stmt = delete(photo).where(photo.c.id == id_photo)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


app.include_router(router)


@app.get("/protected-route")
def protected_route(album_name: str, user: User = Depends(current_user)):
    return f"Hello, {user.email}, id = {user.id}"
