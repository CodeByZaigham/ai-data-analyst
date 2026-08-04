from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    db_path: str
    api_key:str
    api_endpoint:str
    model_config=SettingsConfigDict(env_file = ".env")


settings = Settings()

# -> NOT RELIABLE

# from dotenv import load_dotenv
# import os

# class Settings():
#      db_url=os.getenv("db_path")

# settings=Settings()