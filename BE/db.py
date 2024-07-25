
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,session,Session
from sqlalchemy import create_engine

DATABASE_URL='mysql+pymysql://gabriele:Gabry678@db_mysql/automotosprint'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def init_db():
    from models import clienti, ordine, forniture, prodotto
    Base.metadata.create_all(bind=engine)