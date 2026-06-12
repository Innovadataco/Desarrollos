from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import reportes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Protección Infantil Comunitaria",
    description="API para registro anónimo de reportes de protección infantil.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reportes.router)


@app.get("/api/health", tags=["health"])
def health_check():
    return {"status": "ok"}
