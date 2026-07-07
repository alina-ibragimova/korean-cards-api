from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import cards, auth
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Korean Cards API",
    description="Бэкенд для изучения корейских слов с интервальным повторением",
    version="1.0.0"
)

app.include_router(cards.router)
app.include_router(auth.router)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return FileResponse("static/index.html")