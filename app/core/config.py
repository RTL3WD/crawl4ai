from pydantic import BaseModel

class Settings(BaseModel):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Crawl4AI Service"
    VERSION: str = "1.0.0"

settings = Settings() 