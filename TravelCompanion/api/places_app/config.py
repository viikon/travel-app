import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv()

class Settings(BaseSettings):
    api_key: str = Field(..., validation_alias="API_KEY")
    limit: int = Field(5, validation_alias="LIMIT")
    foursquare_url: str = Field(
        "https://api.foursquare.com/v3/places/search",
        validation_alias="FOURSQUARE_URL"
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }

    @property
    def headers(self):
        return {
            "accept": "application/json",
            "Authorization": self.api_key,
        }

settings = Settings()
