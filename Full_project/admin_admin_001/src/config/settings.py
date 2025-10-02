# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     PROJECT_NAME: str = "Admin Dashboard Service"
#     API_V1_PREFIX: str = "/api/v1"
#     DATABASE_URL: str
#     JWT_SECRET: str
#     JWT_ALGORITHM: str = "HS256"

#     class Config:
#         env_file = ".env"

# settings = Settings()


# from pydantic import BaseSettings

# import os
# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:1234@localhost:5432/admin_dashboard")
#     admin_api_key: str = os.getenv("ADMIN_API_KEY", "super-secret-admin-key")

#     class Config:
#         env_file = ".env"   # automatically load .env values

# settings = Settings()
