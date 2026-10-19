from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.dev.router import router as dev_router
from src.meetings.adaptors.routers import router as meetings_router

app = FastAPI(title="Meetings API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])
app.include_router(meetings_router)
app.include_router(dev_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
