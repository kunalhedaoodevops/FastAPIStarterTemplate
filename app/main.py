from fastapi import FastAPI

from app.routes import files
from .databases.db import engine
from .databases.seed import run_seed
from .models import base
from .routes import files, users, items, health, graphql
from .routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from starlette_exporter import PrometheusMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import os

BASE_DIR = Path(__file__).resolve().parent

base.Base.metadata.create_all(bind=engine)

description = (BASE_DIR / "DESCRIPTION.md").read_text(encoding="utf-8")

app = FastAPI(
    title="FastAPI Starter Template",
    description=description,
    summary="Ready template for the project.",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Kunal Hedaoo",
        "url": "http://kunaltechdesign.page.gd/",
        "email": "kunalhedaoodevops@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus middleware stays here
app.add_middleware(PrometheusMiddleware)

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

@app.on_event("startup")
async def startup():
    if os.getenv("RUN_SEED") == "true":
        run_seed()
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app.include_router(auth_router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(files.router)
app.include_router(health.router)
app.include_router(graphql.graphql_app, prefix="/graphql", tags=["GraphQL"])
