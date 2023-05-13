from fastapi import FastAPI, APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from auth.database import User
import sys

sys.path.insert(0, './proto')
from proto.grpc_client import grpc_client

client = grpc_client() # gRPC S3-backend client

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
async def add_photo(
        id_album: int,
        id_photo: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return "You added photo ..."

app.include_router(router)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"