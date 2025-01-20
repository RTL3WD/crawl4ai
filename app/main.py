from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A web crawling service powered by Crawl4AI",
    version=settings.VERSION,
)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Crawl4AI Service"} 