from fastapi import FastAPI

import db.init_db

app = FastAPI()


@app.get("/ping/")
def ping():

    return {"status": "active"}
