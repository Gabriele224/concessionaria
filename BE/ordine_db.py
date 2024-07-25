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

class ordineCreate(BaseModel):
    cliente:int
    data:date

class ordineUpdate(BaseModel):
    cliente:int
    data:date
    
    class Config:
        orm_mode = True
#sessione database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Ottenimento tutti gli ordini
@router.get("/ordine")
def ordini(db:Session=Depends(get_db)):
    ord= db.query(ordine).all()
    return ord
#1)Elenco degli ordini effettuati da uno specifico cliente:
@router.get("/ordini/{name}")
def ordini(name:str,db: Session = Depends(get_db)):
        ord = db.query(ordine.codordine).select_from(ordine).join(clienti,ordine.cliente==clienti.clientiId).filter(clienti.nome== name).first()
        ordine_cliente=[{'codordine':codordine} for codordine in ord]
        return ordine_cliente

#3)Elenco degli ordini dei rispettivi clienti 
#con importo complessivo organizzato per importo
@router.get("/ordine_clienti")
def ordine_clienti(db:Session=Depends(get_db)):
    result=db.query(clienti.nome,ordine.codordine
                    ,func.sum(forniture.qt * prodotto.prezzoprod
                                                           ).label('TOT')).select_from(ordine
                                                                                       ).join(clienti,ordine.cliente==clienti.clientiId
                                                                                              ).join(forniture,ordine.codordine==forniture.codordine
                                                                                                     ).join(prodotto,forniture.codiceprod==prodotto.codiceprod
                                                                                                            ).group_by(clienti.nome,ordine.codordine)
    totale=[{'nome':nome,'codordine':codordine,'TOT':TOT} for nome,codordine,TOT in result]
    return totale

#4)indica il numero e la data di tutti gli ordini dove è 
# stato venduto uno specifico e il numero di 
# pezzi di quel prodotto venduti

@router.get("/ordine_venduti/{product}")
def ordine_venduti(product:str,db:Session=Depends(get_db)):
    result=db.query(ordine.codordine,forniture.qt).select_from(forniture
                                                               ).join(ordine,forniture.codordine==ordine.codordine
                                                                      ).join(prodotto,forniture.codiceprod==prodotto.codiceprod
                                                                             ).filter(prodotto.nomeprod==product).all()
    ord_venduti=[{'codordine':codordine,'qt':qt} for codordine,qt in result]
    return ord_venduti

#7)quali sono gli ordini che hanno più di un prodotto
@router.get("/ordine_with_prodotto")
def ordine_with_prodotto(db:Session=Depends(get_db)):
    result=db.query(ordine.codordine,func.count().label('PiuProdotti')
                    ).select_from(ordine
                                  ).join(forniture,ordine.codordine==forniture.codordine
                                         ).group_by(ordine.codordine)
    ord_with_product=[{'codordine':codordine,'PiuProdotti':PiuProdotti} for codordine,PiuProdotti in result]
    return ord_with_product

#Ottenimento di un singolo ordine
@router.get("/ordine_singolo/{codice_ordine}")
def cliente_singolo(codice_ordine:int,db:Session=Depends(get_db)):
    cod_ord=db.query(ordine.codordine,ordine.cliente,ordine.data).select_from(ordine).filter(ordine.codordine==codice_ordine).all()
    response_serializable=[
        {
            "codordine":codordine,
            "cliente":cliente,
            "data":data
        } for codordine,cliente,data in cod_ord
        ]
    return response_serializable

#Aggiunta di un ordine

@router.post("/ordini",response_model=ordineCreate)
def ordini(ordini:ordineCreate,db:Session=Depends(get_db)):
    db_ordini=ordine(cliente=ordini.cliente,data=ordini.data)
    db.add(db_ordini)
    db.commit()
    db.refresh(db_ordini)
    return {"message":f"L'ordine {db_ordini} è stato aggiunto"},200

#Aggiornamento dell'ordine
@router.put("/ordini/{codice_ordine}")
def ordini_aggiornamento(codice_ordine:int,ordine_update:ordineUpdate,db:Session=Depends(get_db)):
    db_ordini=db.query(ordine).filter(ordine.codordine==codice_ordine).first()
    db_ordini.cliente=ordine_update.cliente
    db_ordini.data=ordine_update.data
    db.commit()
    db.refresh(db_ordini)
    return {"message":f"Ordine modificato {db_ordini} con successo"}

#Rimozione intero ordine
@router.delete("/ordini/{delete_ord}")
def delete(delete_ord:int,db:Session=Depends(get_db)):
    db_ord=db.query(ordine).filter(ordine.codordine==delete_ord).first()
    db.delete()
    db.commit()
    return {"message":f"L'ordine {db_ord} eliminato con successo"},200