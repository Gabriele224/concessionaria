from datetime import date
from sqlalchemy import Column,Integer,String,ForeignKey,Date
from db import Base
class clienti(Base): ## nome classi lettera grande
    __tablename__="clienti"
    clientiId= Column(Integer, primary_key=True,index=True)
    nome=Column(String(45), nullable=False)
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class ordine(Base):
    __tablename__="ordine"
    codordine=Column(Integer, primary_key=True)
    cliente=Column(Integer, ForeignKey('clienti.clientiId'), nullable=False)
    data=Column(Date,default=date)

class forniture(Base):
    __tablename__="forniture"
    idforniture=Column(Integer,primary_key=True)
    codordine=Column(Integer ,ForeignKey('ordine.codordine'),nullable=False)
    codiceprod=Column(Integer,ForeignKey('prodotto.codiceprod'),nullable=False)
    qt=Column(Integer)

class prodotto(Base):
    __tablename__="prodotto"
    codiceprod=Column(Integer,primary_key=True)
    nomeprod=Column(String(45),nullable=False)
    prezzoprod=Column(Integer)
    giacenza=Column(Integer)