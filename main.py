from fastapi import FastAPI

from api.endpoints.auth import auth_router
from api.endpoints.user import user_router
from api.endpoints.chat import chat_router
from api.endpoints.admin import admin_router
from ws.endpoints.chat_ws import chat_ws

import db.init_db

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")
app.include_router(user_router, prefix="/api/user")
app.include_router(chat_router, prefix="/api/chat")
app.include_router(admin_router, prefix="/api/admin")
app.include_router(chat_ws, prefix="/ws")


@app.get("/ping/")
async def ping():

    return {"status": "active"}
