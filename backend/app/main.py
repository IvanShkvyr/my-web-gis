from fastapi import FastAPI

app = FastAPI(title="My Web GIS API")

@app.get("/")
async def root():
    return {"status": "working", "database": "waiting for config"}

# uvicorn backend.app.main:app --reload
