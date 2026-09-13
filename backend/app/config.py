import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
  ''' Base application config '''  
  
  SQLACHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  
  ACCESS_EXPIRES = timedelta(hours=1)
  
  JWT_SECRET_KEY = os.getenv("JWT_SECRET") 
  JWT_TOKEN_LOCATION = ['cookies']
  JWT_COOKIE_SECURE = False 
  JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
  JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
  JWT_COOKIE_CSRF_PROTECT = True
  
  REDIS_DB = 0
  REDIS_HOST = os.getenv("REDIS_HOST")
  REDIS_PORT = os.getenv("REDIS_PORT")
  
  CORS_ORIGINS = ["http://localhost:5173"]
  CORS_ALLOW_HEADERS = ["Authorization", "Content-Type"]
  CORS_SUPPORTS_CREDENTIALS = True

class DevelopmentConfig(Config):
  DEBUG = True
  DEV_HOST = os.getenv('DEV_HOST')

class ProductionConfig(Config):
  DEBUG = False
  JWT_COOKIE_SECURE = True
  PROD_HOST = os.getenv('PROD_HOST')