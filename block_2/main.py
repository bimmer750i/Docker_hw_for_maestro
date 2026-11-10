import fastapi

app = fastapi.FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/maestro")
async def maestro():
    return {"Maestro is awesome!"}
