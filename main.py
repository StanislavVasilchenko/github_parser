from fastapi import FastAPI

from config.db import database
from routers.repos import router as repos_router

app = FastAPI()
app.include_router(repos_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
