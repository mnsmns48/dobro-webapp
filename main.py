import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from routers import pages_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=f"static"), name="static")
app.include_router(pages_router, tags=["page"])


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000)