import fastapi

app = fastapi.FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}