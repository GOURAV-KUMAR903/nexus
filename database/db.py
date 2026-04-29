# database/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "mysql+pymysql://root:@localhost/python"
DATABASE_URL = "postgresql://nexus_qk8j_user:GspjKn5Rk7P1WopYcFUWliyA6OPSsHsu@dpg-d7optnsm0tmc73d9o2ng-a.virginia-postgres.render.com/nexus_qk8j"


engine = create_engine(DATABASE_URL, echo=True)  # echo=True optional, queries print karega

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()