import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# database_name = os.environ.get('DATABASE_NAME') if os.environ.get('DATABASE_NAME') else '<database name>'
# database_username = os.environ.get('DATABASE_USERNAME') if os.environ.get('DATABASE_USERNAME') else '<database username>'
# database_password = os.environ.get('DATABSE_PASSWORD') if os.environ.get('DATABSE_PASSWORD') else '<database password>'
# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{database_username}:{database_password}@127.0.0.1:3306/{database_name}"

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=3600, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()