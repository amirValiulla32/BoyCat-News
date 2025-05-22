from fastapi import FastAPI
from routes.news import router as news_router
##from mangum import Mangum
app = FastAPI()
app.include_router(news_router)

@app.get("/")
def read_root():
    return {"message": "Boycat News Microservice is running!"}

##handler = Mangum(app)