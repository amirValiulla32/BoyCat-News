from fastapi import FastAPI
from mangum import Mangum
from routes.news import router as news_router

app = FastAPI()
app.include_router(news_router)

@app.get("/")
def read_root():
    return {"message": "Boycat News Microservice is running!"}

# Only for AWS Lambda — ignored locally
handler = Mangum(app)
