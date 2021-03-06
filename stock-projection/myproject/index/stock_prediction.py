import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.keras.layers import Dense,LSTM,Dropout
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers
import matplotlib.pyplot as plt
import tensorflow as tf
import datetime as dt
import yfinance as yf
import pandas as pd
import numpy as np
import threading
import pickle
import math

from django.http import HttpResponse

import warnings
warnings.filterwarnings("ignore")

def stock_prediction(company,exchange):
    import nsepy
    company = str(company).upper()

    start = dt.datetime(2012,1,1)
    end = dt.datetime.today()
    print(company=='TCS')
    if exchange == "US":
        data = yf.download(company, start = start, end=end)
    elif exchange == "IND":
        data = nsepy.get_history(symbol=company,
                   start=start,
                   end=end)
    else:
        print("Error")
        return {}
    
    if data.empty:
        print("dataframe is empty")
        return {}

    data = data.filter(['Close'])
    dataset = data.values
    train_dataset_len = math.ceil(len(dataset)*.8)

    scaler = MinMaxScaler((0,1))
    scaled_data = scaler.fit_transform(dataset)
    train_data = scaled_data[:train_dataset_len, :]

    prediction_days = 60
    x_train = []
    y_train = []
    for i in range(prediction_days,len(train_data)):
        x_train.append(train_data[i-prediction_days:i,0])
        y_train.append(train_data[i,0])
    x_train,y_train = np.array(x_train),np.array(y_train)
    x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))

    filename = "stock_prediction.h5"
    if( not "saved_models" in os.listdir()):
        os.mkdir("saved_models")
        
    if True:
        model = Sequential()
        model.add(LSTM(50,return_sequences=True, input_shape=(x_train.shape[1],1)))
        model.add(Dropout(0.2))
        model.add(LSTM(50,return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(50,return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(50))
        model.add(Dropout(0.2))
        model.add(Dense(1))

        model.compile(optimizer='adam',loss='mean_squared_error')
        #epochs 30minimum
        model.fit(x_train,y_train, epochs=30,batch_size=32)
        filename = os.path.join("saved_models","stock_prediction.h5")
        model.save(filepath=filename)



    test_data = scaled_data[train_dataset_len - prediction_days:,:]
    x_test = []
    y_test = dataset[train_dataset_len:,:]
    for i in range(prediction_days,len(test_data)):
        x_test.append(test_data[i-prediction_days:i,0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    # root mean squered error
    rmse = np.sqrt(np.mean(predictions-y_test)**2)
    rmse

    train = data[:train_dataset_len]
    valid = data[train_dataset_len:]
    valid['Predictions'] = predictions

    x_input = scaled_data[scaled_data.shape[0] - prediction_days :].reshape(1,-1)
    temp_input=list(x_input)
    temp_input=temp_input[0].tolist()

    # demonstrate prediction for next 10 days
    from numpy import array

    lst_output=[]
    n_steps=60
    i=0
    while(i<30):
        
        if(len(temp_input)>n_steps):
            #print(temp_input)
            x_input=np.array(temp_input[1:])
            print("{} day input {}".format(i,x_input))
            x_input=x_input.reshape(1,-1)
            x_input = x_input.reshape((1, n_steps, 1))
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input=temp_input[1:]
            #print(temp_input)
            lst_output.extend(yhat.tolist())
            i=i+1
        else:
            x_input = x_input.reshape((1, n_steps,1))
            yhat = model.predict(x_input, verbose=0)
            print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i=i+1
        

    print(lst_output)


    lst_output = scaler.inverse_transform(lst_output)
    temp_data = x_input.reshape(-1,1)
    temp_data = scaler.inverse_transform(temp_data)

    #plt.plot(temp_data)
    #plt.show()
    predicted_prices = temp_data[-15:]
    graphs = {}
    graphs["output"] = temp_data
    graphs["prediction"] = predicted_prices

    return graphs
