# -*- coding: utf-8 -*-

import math
import pandas as pd
import numpy as np
import tushare as ts
import datetime

df = ts.get_today_all()
file_name = str(datetime.date.today()) + '_Astock.csv'
df.to_csv('./data/'+file_name)