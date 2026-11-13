from fastapi import FastAPI
from db_engine import Database
from contextlib import asynccontextmanager

# app = FastAPI()
# db = Database()

# @app.get("/")
# async def root():
#     return {"i'm working, nigga"}
db = Database()

@asynccontextmanager
async def lifespan(app : FastAPI):
    await db.init_db()
    yield
    await db.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_clicks():
    response = await db.increment_and_get_clicks()
    return response

@app.get("/reset")
async def reset_clicks():
    response = await db.reset_and_get_clicks()
    return response

@app.get("/health")
async def get_health():
    return {"healthy"}