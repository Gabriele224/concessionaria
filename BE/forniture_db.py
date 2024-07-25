from fastapi import FastAPI,HTTPException, Depends,APIRouter
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from db import SessionLocal
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session,mapped_column,Mapped
from pydantic import BaseModel
from typing import List
from sqlalchemy import Text,Date,func,desc
from datetime import date
from models import clienti,ordine,forniture,prodotto
router = InferringRouter()

class fornituraCreate(BaseModel):
    codordine:int
    codiceprod:int
    qt:int

class fornituraUpdate(BaseModel):
    codordine:int
    codiceprod:int
    qt:int

    class Config:
        orm_mode = True
#sessione database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#1)Ottenimento di tutte le forniture
@router.get("/fornitura")
def fornitura(db:Session=Depends(get_db)):
    f=db.query(forniture).all()
    return f

#2)Ottenimento di una singola fornitura
@router.get("/fornitura/{id}")
def fornitura(id:int,db:Session=Depends(get_db)):
    forni=db.query(forniture.idforniture,forniture.codordine,forniture.codiceprod,forniture.qt
                   ).select_from(forniture
                                 ).filter(forniture.idforniture==id).all()
    response_serializable=[
        {
            "idforniture":idforniture,
            "codordine":codordine,
            "codiceprod":codiceprod,
            "qt":qt
        } for idforniture, codordine,codiceprod,qt in forni
        ]
    return response_serializable

#Aggiunta fornitura
@router.post("/fornitura",response_model=fornituraCreate)
def fornitura(forni:fornituraCreate,db:Session=Depends(get_db)):
    db_fornitura=forniture(codordine=forni.codordine,codiceprod=forni.codiceprod,qt=forni.qt)
    db.add(db_fornitura)
    db.commit()
    db.refresh(db_fornitura)
    return db_fornitura

#Aggiornamento della fornitura
@router.put("/fornitura/{id}")
def fornitura_aggiornamento(id:int,fornitura_update:fornituraUpdate,db:Session=Depends(get_db)):
    db_fornitura=db.query(forniture).filter(forniture.idforniture==id).first()
    db_fornitura.codordine=fornitura_update.codordine
    db_fornitura.codiceprod=fornitura_update.codiceprod
    db_fornitura.qt=fornitura_update.qt
    db.commit()
    db.refresh(db_fornitura)
    return db_fornitura

#Rimozione della fornitura
@router.delete("/fornitura/{delete_forni}")
def delete(delete_forni:int,db:Session=Depends(get_db)):
    db_forni=db.query(forniture).filter(forniture.idforniture==delete_forni).first()
    db.delete()
    db.commit()
    return {"message":f"L'ordine {db_forni} eliminato con successo"},200
