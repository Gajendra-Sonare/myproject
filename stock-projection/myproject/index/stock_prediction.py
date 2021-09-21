import datetime as dt
import yfinance as yf
import pandas as pd
import numpy as np
import threading
import warnings
import math
import os

warnings.filterwarnings("ignore")

def stock_prediction(company):

    #company = 'TSLA'
    start = dt.datetime(2012,1,1)
    end = dt.datetime(2020,1,1)
    data = yf.download(company, start = start, end=end)


    data = data.filter(['Close'])
    return data