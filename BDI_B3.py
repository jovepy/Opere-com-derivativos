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


n=0
while r.status_code != 200:
    BDI_DIA = (date.today()-timedelta(n)).strftime('%Y%m%d')
    url = 'https://up2dataweb.blob.core.windows.net/bdi/BDI_00_{}.pdf'.format(BDI_DIA)
    r = requests.get(url,stream=True)
    aux = r.status_code
    if aux == 200:
        filename = Path(r'C:\Users\rodrigo.jove\Documents\PC_ET\Opere-com-derivativos\temp\BDI_DIA.pdf')
        filename.write_bytes(r.content)
            
    n+=1

BDI = extract_text(filename)
