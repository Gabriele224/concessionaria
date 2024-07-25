import sys,os
import streamlit as st
import requests
from datetime import date

# url per le fastapi

BASE_URL= "http://backend:8000"

#funzioni per le api

def get_simple(Query):
    response=requests.get(f"{BASE_URL}/{Query}")
    return response.json()
    

def clienti_total(clienti_box):
    response=requests.get(f"{BASE_URL}/{clienti_box}")
    return response.json()

def nomi_or_id(query_nome,nome_query_nome_id):
    response=requests.get(f"{BASE_URL}/{query_nome}/{nome_query_nome_id}")
    return response.json()

def get_ordine_total(ordine_box,serie_box):
    response=requests.get(f"{BASE_URL}/{ordine_box}/{serie_box}")
    return response.json()

def simple_ordine(ord_box):
    response=requests.get(f"{BASE_URL}/{ord_box}")
    return response.json()

def prodotto_get(proquery):
    response=requests.get(f"{BASE_URL}/{proquery}")
    return response.json()

def single_c_o_f_p(cofp,single):
    response=requests.get(f"{BASE_URL}/{cofp}/{single}")
    return response.json()

def post_c_o_f_p(pcofp,data):
    if "data" in data and isinstance(data["data"], date):
        data["data"] = data["data"].isoformat()
    response=requests.post(f"{BASE_URL}/{pcofp}",json=data)
    return response

def put_c_o_f_p(putcofp,identificativo,data):
    if "data" in data and isinstance(data["data"], date):
        data["data"] = data["data"].isoformat()
    response=requests.put(f"{BASE_URL}/{putcofp}/{identificativo}",json=data)
    return response

def delete_c_o_f_p(deletecofp,iden):
    response=requests.delete(f"{BASE_URL}/{deletecofp}/{iden}")
    return response.json()