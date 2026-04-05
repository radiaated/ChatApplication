from fastapi import FastAPI

from api.endpoints.auth import auth_router

import db.init_db

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")


@app.get("/ping/")
async def ping():

    return {"status": "active"}
