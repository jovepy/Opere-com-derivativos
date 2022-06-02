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
        
dfs = tabula.read_pdf("temp\BDI_DIA.pdf", pages='all')

dfs[0]
