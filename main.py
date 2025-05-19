from fastapi import FastAPI
from routes.news import router as news_router
print(" Importing news_router...")
app = FastAPI()
app.include_router(news_router)
print(" news_router included!")  
@app.get("/")
def read_root():
    return {"message": "Boycat News Microservice is running!"}