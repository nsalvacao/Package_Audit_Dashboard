"""Aplicação FastAPI principal do Package Audit Dashboard."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import discover, managers, packages


def create_app() -> FastAPI:
    app = FastAPI(
        title="Package Audit Dashboard API",
        version="0.1.0",
        description="API para descoberta e gestão de gestores de pacotes.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(discover.router)
    app.include_router(managers.router)
    app.include_router(packages.router)
    return app


app = create_app()
