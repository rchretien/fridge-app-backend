"""Main entrypoint for the API."""

import os
from collections.abc import Callable
from datetime import datetime
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pytz import timezone

from fridge_app_backend.api.routes.inventory_routes import inventory_router

API_NAME = "Fridge Inventory App Backend"
API_DESCRIPTION = "CRUD API for managing a fridge inventory."
API_VERSION = "0.1.0"
BRUSSELS_TZ = timezone("Europe/Brussels")


app = FastAPI(
    title=API_NAME,
    description=API_DESCRIPTION,
    started=datetime.now(tz=BRUSSELS_TZ),
    version=API_VERSION,
)

app.include_router(inventory_router)


@app.middleware("http")
async def add_headers(request: Request, call_next: Callable[..., Any]) -> Response:
    """
    Add process time and security headers.

    Middleware to add extra headers to report the time required to execute
    an API call and several security headers.
    """
    start_time = datetime.now(tz=BRUSSELS_TZ)
    response: Response = await call_next(request)
    process_time = datetime.now(tz=BRUSSELS_TZ) - start_time

    # Inject security headers
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "sameorigin"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"

    return response


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Redirect response to docs
@app.get("/", include_in_schema=False, response_class=Response)
def go_to_docs() -> Response:
    """Redirect to docs."""
    return RedirectResponse(url="/docs")


@app.get("/index", include_in_schema=False)
async def index() -> dict[str, str | list[str]]:
    """Index API Call."""
    return {
        "Title": app.title,
        "Description": app.description,
        "started": app.extra["started"].isoformat(),
        "Git commit": os.environ.get("COMMIT", "not set"),
        "Git branch": os.environ.get("BRANCH", "not set"),
    }
