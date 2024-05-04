from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers import dobrotsen_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")
app.include_router(dobrotsen_router, tags=["page"])