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

class prodottoCreate(BaseModel):
    nomeprod:str
    prezzoprod:int
    giacenza:int

class prodottoUpdate(BaseModel):
    nomeprod:str
    prezzoprod:int
    giacenza:int

    class Config:
        orm_mode = True
#sessione database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Ottenimento di tutti i prodotti
@router.get("/prodotti")
def prodotti(db:Session=Depends(get_db)):
    p=db.query(prodotto).all()
    return p

#Ottenimento di un singolo prodotto
@router.get("/prodotto_single/{codice}")
def prodotto_single(codice:int,db:Session=Depends(get_db)):
    prod=db.query(prodotto.codiceprod,prodotto.nomeprod,prodotto.prezzoprod,
                  prodotto.giacenza).select_from(prodotto).filter(prodotto.codiceprod==codice).all()
    p=[{'codiceprod':codiceprod,'nomeprod':nomeprod,
        'prezzoprod':prezzoprod,'giacenza':giacenza}
         for codiceprod,nomeprod,prezzoprod,giacenza in prod]
    return p

#1)Elenco dei prodotti più venduti in base alla quantità totale venduta
@router.get("/prodotti_qt")
def prodotti_qt(db:Session=Depends(get_db)):
    prod=db.query(prodotto.nomeprod,
                  func.sum(forniture.qt).label('totale_quantità')
                  ).select_from(prodotto).outerjoin(forniture,prodotto.codiceprod==forniture.codiceprod
                                                    ).group_by(prodotto.nomeprod
                                                               ).filter(prodotto.nomeprod.isnot(None)
                                                                        ).order_by(desc('totale_quantità')).all()
    p=[{'nomeprod':nomeprod,'totale_quantità':totale_quantità} 
       for nomeprod,totale_quantità in prod]
    return p

#2)prodotti non ancora ordinati da nessun cliente
@router.get("/prodotti_no_ordinati")
def prodotti_no_ordinati(db:Session=Depends(get_db)):
    subquery=db.query(forniture.codiceprod).distinct().subquery()

    p_no_o=db.query(prodotto.codiceprod,prodotto.nomeprod
                    ).outerjoin(subquery,prodotto.codiceprod==subquery.c.codiceprod
                                ).filter(subquery.c.codiceprod==None).all()
    p=[{'codiceprod':codiceprod,'nomeprod':nomeprod} for codiceprod,nomeprod in p_no_o]
    return p

#Aggiunta prodotto
@router.post("/prodotti",response_model=prodottoCreate)
def prodotti(prodotti:prodottoCreate,db:Session=Depends(get_db)):
    db_prodotti=prodotto(nomeprod=prodotti.nomeprod,prezzoprod=prodotti.prezzoprod,giacenza=prodotti.giacenza)
    db.add(db_prodotti)
    db.commit()
    db.refresh(db_prodotti)
    return db_prodotti

#Aggiornamento dell'ordine
@router.put("/prodotti/{id}")
def prodotti_aggiornamento(id:int,prodotto_update:prodottoUpdate,db:Session=Depends(get_db)):
    db_prodotto=db.query(prodotto).filter(prodotto.codiceprod==id).first()
    db_prodotto.nomeprod=prodotto_update.nomeprod
    db_prodotto.prezzoprod=prodotto_update.prezzoprod
    db_prodotto.giacenza=prodotto_update.giacenza
    db.commit()
    db.refresh(db_prodotto)
    return db_prodotto

#Rimozione intero ordine
@router.delete("/prodotti/{delete_prod}")
def delete(delete_prod:int,db:Session=Depends(get_db)):
    db_prod=db.query(prodotto).filter(prodotto.codiceprod==delete_prod).first()
    db.delete()
    db.commit()
    return {"message":f"L'ordine {db_prod} eliminato con successo"},200