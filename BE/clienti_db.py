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

#pyndatic
class clienteCreate(BaseModel):
    nome:str

class ClienteUpdate(BaseModel):
    nome:str

    class Config:
        orm_mode = True
#sessione database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#1)Ottieni tutti gli utenti
@router.get("/clienti")
def cliente(db: Session = Depends(get_db)):
   client = db.query(clienti).all()
   return client

#2)Elenco dei clienti che comprano uno specifico prodotto
@router.get("/clienti_with_prodotto/{product}")
def clienti_with_prodotto(product:str,db:Session=Depends(get_db)):
    product=db.query(clienti).join(ordine).join(forniture).join(prodotto).filter(prodotto.nomeprod==product).all()
    return product

#3)Elenca i clienti indicando quanti ordini hanno effettuato
@router.get("/ordine_clienti")
def ordine_clienti(db:Session=Depends(get_db)):
    ord_effettuati=db.query(clienti.nome,func.count().label('tot_ordini')).select_from(ordine).join(clienti).group_by(clienti.clientiId)
    response_serializable=[
        {
            "nome":nome,
            "tot_ordini":tot_ordini

        } for nome,tot_ordini in ord_effettuati
        ]
    return response_serializable

#4)Elenca i clienti indicando il quantitativo di pezzi acquistato
@router.get("/clienti_acquisto")
def clienti_acquisto(db:Session=Depends(get_db)):
    client_acquist=db.query(clienti.nome, func.sum(forniture.qt).label('Quantità')).select_from(ordine).join(clienti).join(forniture).group_by(clienti.nome)
    response_serializable=[
        {
            "nome":nome,
            "Quantità":Quantità
        } for nome,Quantità in client_acquist
        ]
    return response_serializable
#5)Ottenimento cliente singolo
@router.get("/cliente_singolo/{client}")
def cliente_singolo(client:int,db:Session=Depends(get_db)):
    client_single=db.query(clienti.clientiId,clienti.nome).select_from(clienti).filter(clienti.clientiId==client).all()
    response_serializable=[
        {
            "clientiId":clientiId,
            "nome":nome
        } for clientiId,nome in client_single
        ]
    return response_serializable
#6)Elenco dei prodotti acquistati da un cliente specifico e la quantità acquistata
@router.get("/cliente_prodotto/{nome_cliente}")
def cliente_prodotto(nome_cliente:str,db:Session=Depends(get_db)):
    client_product=db.query(clienti.nome,prodotto.nomeprod,forniture.qt).select_from(clienti
                                          ).join(ordine,clienti.clientiId==ordine.cliente).join(forniture,
                                                                                                ordine.codordine==forniture.codordine
                                                              ).join(prodotto,forniture.codiceprod==prodotto.codiceprod
                                                                     ).filter(clienti.nome==nome_cliente).all()
    response_serializable=[
           {
            
               
               "nomeprod":nomeprod,
               "nome": nome,
               "qt":qt
           }
           for nomeprod,nome,qt in client_product
       ]
    return response_serializable
    
#7)Elenco dei clienti che hanno speso di più in totale
@router.get("/cliente_spesa")
def cliente_spesa(db:Session=Depends(get_db)):
    client_shop=db.query(clienti.nome.label('cliente'),func.sum(prodotto.prezzoprod.label('Spesa_cliente'))).select_from(clienti).join(ordine,clienti.clientiId==ordine.cliente).join(forniture,ordine.codordine==forniture.codordine).join(prodotto,forniture.codiceprod==prodotto.codiceprod).group_by(clienti.nome)
    response_serializable=[
           {
            
               "cliente": nome,
               "Spesa_cliente":prezzoprod
              
           }
           for nome,prezzoprod in client_shop
       ]
    return response_serializable


#Aggiunta di un nuovo cliente
@router.post("/clienti",response_model=clienteCreate)
def aggiungi_cliente(cliente:clienteCreate,db:Session=Depends(get_db)):
     db_cliente=clienti(nome=cliente.nome)
     db.add(db_cliente)
     db.commit()
     db.refresh(db_cliente)
     return db_cliente

#Modifica un seguente cliente
@router.route("/clienti/{clientiId}")
class Crudclienti():
    @router.put("/clienti/{clientiId}")
    def aggiornamento(clientiId:int,cliente_update:ClienteUpdate, db:Session=Depends(get_db)):
        db_cliente=db.query(clienti).filter(clienti.clientiId==clientiId).first()
        db_cliente.nome=cliente_update.nome
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
#Rimozione cliente
    @router.delete("/clienti/{clientiId}")
    def delete_cliente(clientiId:int,db:Session=Depends(get_db)):
        db_cliente=db.query(clienti).filter(clienti.clientiId==clientiId).first()
        db.delete(db_cliente)
        db.commit()
        return {"message":f"il cliente è stato eliminato {clientiId}"},200
