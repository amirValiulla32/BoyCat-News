from fastapi import FastAPI
##from mangum import Mangum
from app.rss.news import router as news_router

app = FastAPI()
app.include_router(news_router)

@app.get("/")
def read_root():
    return {"message": "Boycat News Microservice is running!"}

from app.routes.cron import router as cron_router
app.include_router(cron_router, prefix="/internal")
