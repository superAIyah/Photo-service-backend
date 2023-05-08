from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import insert, select
from models.models import test

app = FastAPI()


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

@app.get("/")
async def root():
    return "Backend image service by @FedorX8"

# @app.get("/{folder}")
# async def get_ids_by_folder(user_id: str, folder: str):
#     ids = []
#     result = {"ids": ids}
#     ids.append(f"test_id_for_all_images_{user_id}_{folder}")
#     return result
#
# @app.get("/{folder}/{image}")
# async def get_id_by_image(user_id: str, folder: str, image: str):
#     ids = []
#     result = {"ids": ids}
#     ids.append(f"test_id_for_all_images_{user_id}_{folder}_{image}")
#     return result


@app.get("/test")
async def paste_test(session: AsyncSession = Depends(get_async_session)):
    # query = select(test).where(test.c.name == name)
    # result = await session.execute(query)
    # print(result.all())
    stmt = insert(test).values(name="username", age=27)
    await session.execute(stmt)
    await session.commit()
    return "OK"

@app.get("/ret")
async def func():
    return "OK"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)