from fastapi import FastAPI, Depends
import uvicorn
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from auth.database import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)