# -*- coding: utf-8 -*-
"""
Created on Sat May 14 10:50:13 2022

@author: rodrigo.jove
"""

import requests
from pathlib import Path
from datetime import date, timedelta
import pandas as pd
import numpy as np
import tabula

n=0
BDI_DIA = (date.today()-timedelta(n)).strftime('%Y%m%d')
url = 'https://up2dataweb.blob.core.windows.net/bdi/BDI_03-2_{}.pdf'.format(BDI_DIA)
aux = requests.get(url,stream=True)
while aux != 200:
    BDI_DIA = (date.today()-timedelta(n)).strftime('%Y%m%d')
    url = 'https://up2dataweb.blob.core.windows.net/bdi/BDI_03-2_{}.pdf'.format(BDI_DIA)
    r = requests.get(url,stream=True)
    aux = r.status_code            
    n+=1
if aux == 200:
        filename = Path(r'temp\BDI_DIA.pdf')
        filename.write_bytes(r.content)
        
dfs = tabula.read_pdf("temp\BDI_DIA.pdf", pages='all', pandas_options=({'header': None}))


df = pd.DataFrame()
for i in dfs:
    df = pd.concat([df,i],axis=0)

df1 = pd.DataFrame()
for coluna in df:
    df2 = pd.DataFrame()
    aux= pd.DataFrame(df[coluna].str.split(' ',expand=True))
    aux.columns = list(range(coluna,coluna+len(aux.columns)))
    df1 = pd.concat([df1,aux],axis=1)
    
df1.to_excel('ver.xlsx')
df1 = df1.set_index(0)

tickers = []
vencimentos = [] 
for ticker in df1.index:
    for i in df1.loc[ticker]:
        try:
            ano = date.today().strftime("%Y")
            if ano in i:
                for n in list(range(len(i))):
                    if i[n:n+(len('/{}'.format(ano)))] == '/{}'.format(ano):
                        vencimentos.append(i[len('xx/xx/xxxx')*-1:n+len('/{}'.format(ano))])
                        tickers.append(ticker)
        except Exception as e:
            pass



df_estruturado = pd.DataFrame()
for ticker, vencimento in zip(tickers,vencimentos):
    aux = (list(df1.loc[ticker].dropna()))[-11:] 
    while ano in aux[0]:
        aux=aux[1:]
        aux[-1] = '-'
    aux = pd.DataFrame([ticker,vencimento]+aux).T
    df_estruturado = pd.concat([df_estruturado,aux],axis=0)
    
df_estruturado = df_estruturado[df_estruturado.columns[:-2]] #exclui-se as colunas de negócios realizados, pois não quero nenhum viés de mercado

    
df_estruturado.columns = ['Código' ,'Vencimento' ,'Exercício','Abertura' ,'Mínimo','Máximo', 'Médio' ,'Fechamento', 'Oscilação (%)','Compra (R$)' ,'Venda (R$)']
