from fastapi import FastAPI,HTTPException, Depends
from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session,mapped_column,Mapped
from pydantic import BaseModel
from typing import List
from sqlalchemy import Text,Date,func,desc
from datetime import date
from clienti_db import router as Clienti_router
from ordine_db import router as Ordine_router
from forniture_db import router as Froniture_router
from prodotto_db import router as Prodotto_router
from db import  DATABASE_URL,init_db
app = FastAPI()

DATABASE_URL="mysql+pymysql://gabriele:Gabry678@db_mysql/automotosprint"
sessionmaker = FastAPISessionMaker(DATABASE_URL)

@app.on_event("startup")
async def on_startup():
    init_db()

app.include_router(Clienti_router)
app.include_router(Ordine_router)
app.include_router(Froniture_router)
app.include_router(Prodotto_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")