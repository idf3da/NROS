import math
import pickle
import random

import keras.layers as kl
import keras.models as km
import numpy as np
import pandas as pd
from keras import backend as K
# import matplotlib.pyplot as plt
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler


# import keras.backend.tensorflow_backend as tb
# tb._SYMBOLIC_SCOPE.value = True

# from scipy.optimize import fmin

def trainModels(inData, before_range, type_id, models):
    # print(data['Quantity'] != data['Quantity'].min())
    data = pd.DataFrame(columns = {'Quantity','date'})

    for sale in inData:
        if sale.product_item.product_type_id == type_id:
            data = data.append({'Quantity':sale.product_item.count,'date':sale.date}, ignore_index=True)


    # for i in inData:
    #     data = data.append({'Quantity':i[-1].count,'date':i[0].date}, ignore_index=True)

    data = data.set_index(['date'])
    data = data['Quantity'].resample('D').sum()
    print(data)
    slen = len(data[data != min(data)])
    # slen = 1 #для теста
    print(slen,(len(data)*7)//10)
    if slen <= (len(data)*7)//10:
        a,b,g = train(data,slen)
    else:
        a,b,g = -1,-1,-1
    if models == []:
        model,scaler = trainLSTM(data,do_scale = True,epochs = 100,batch = 32,verbose = 0,before_range = before_range)
    else:
        model,scaler = trainLSTM(data,do_scale = True,epochs = 100,batch = 32,verbose = 0,before_range = before_range,models = models)
    return a,b,g,model,scaler

class HoltWinters:
    def __init__(self, series, slen, alpha, beta, gamma, n_preds, scaling_factor=1.96):
        self.series = series
        self.slen = slen
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.n_preds = n_preds
        self.scaling_factor = scaling_factor

    def initial_trend(self):
        sum = 0.0
        for i in range(self.slen):
            sum += float(self.series[i+self.slen] - self.series[i]) / self.slen
        return sum / self.slen

    def initial_seasonal_components(self):
        seasonals = {}
        season_averages = []
        n_seasons = int(len(self.series)/self.slen)
        for j in range(n_seasons):
            season_averages.append(sum(self.series[self.slen*j:self.slen*j+self.slen])/float(self.slen))
        for i in range(self.slen):
            sum_of_vals_over_avg = 0.0
            for j in range(n_seasons):
                sum_of_vals_over_avg += self.series[self.slen*j+i]-season_averages[j]
            seasonals[i] = sum_of_vals_over_avg/n_seasons
        return seasonals

    def triple_exponential_smoothing(self):
        self.result = []
        self.Smooth = []
        self.Season = []
        self.Trend = []
        self.PredictedDeviation = []
        self.UpperBond = []
        self.LowerBond = []

        seasonals = self.initial_seasonal_components()

        for i in range(len(self.series)+self.n_preds):
            if i == 0: # инициализируем значения компонент
                smooth = self.series[0]
                trend = self.initial_trend()
                self.result.append(self.series[0])
                self.Smooth.append(smooth)
                self.Trend.append(trend)
                self.Season.append(seasonals[i%self.slen])

                self.PredictedDeviation.append(0)

                self.UpperBond.append(self.result[0] +
                                      self.scaling_factor *
                                      self.PredictedDeviation[0])

                self.LowerBond.append(self.result[0] -
                                      self.scaling_factor *
                                      self.PredictedDeviation[0])

                continue
            if i >= len(self.series): # прогнозируем
                m = i - len(self.series) + 1
                self.result.append((smooth + m*trend) + seasonals[i%self.slen])

                # во время прогноза с каждым шагом увеличиваем неопределенность
                self.PredictedDeviation.append(self.PredictedDeviation[-1]*1.01)

            else:
                val = self.series[i]
                last_smooth, smooth = smooth, self.alpha*(val-seasonals[i%self.slen]) + (1-self.alpha)*(smooth+trend)
                trend = self.beta * (smooth-last_smooth) + (1-self.beta)*trend
                seasonals[i%self.slen] = self.gamma*(val-smooth) + (1-self.gamma)*seasonals[i%self.slen]
                self.result.append(smooth+trend+seasonals[i%self.slen])

                # Отклонение рассчитывается в соответствии с алгоритмом Брутлага
                self.PredictedDeviation.append(self.gamma * np.abs(self.series[i] - self.result[i])
                                               + (1-self.gamma)*self.PredictedDeviation[-1])

            self.UpperBond.append(self.result[-1] +
                                  self.scaling_factor *
                                  self.PredictedDeviation[-1])

            self.LowerBond.append(self.result[-1] -
                                  self.scaling_factor *
                                  self.PredictedDeviation[-1])

            self.Smooth.append(smooth)
            self.Trend.append(trend)
            self.Season.append(seasonals[i % self.slen])
def timeseriesCVscore(x,data,slen):
    # вектор ошибок
    errors = []

    values = data.values.astype('float64')
    alpha, beta, gamma = x

    # задаём число фолдов для кросс-валидации
    tscv = TimeSeriesSplit(n_splits=2)

    # идем по фолдам, на каждом обучаем модель, строим прогноз на отложенной выборке и считаем ошибку
    for train, test in tscv.split(values):

        print(values[train])

        model = HoltWinters(series=values[train], slen = slen, alpha=alpha, beta=beta, gamma=gamma, n_preds=len(test))
        model.triple_exponential_smoothing()

        predictions = model.result[-len(test):]
        actual = values[test]
        error = mean_squared_error(predictions, actual)
        errors.append(error)

    # Возвращаем средний квадрат ошибки по вектору ошибок 
    return np.mean(np.array(errors))
def train(data,slen):
    x = [0, 0, 0]

    # Минимизируем функцию потерь с ограничениями на параметры
    opt = minimize(timeseriesCVscore, x0=x, args=(data,slen), method="TNC", bounds = ((0, 1), (0, 1), (0, 1)))

    # Из оптимизатора берем оптимальное значение параметров
    alpha_final, beta_final, gamma_final = opt.x
    print(alpha_final, beta_final, gamma_final)
    return alpha_final, beta_final, gamma_final

def transform_data_train(resC,before_range):
    resC = resC.reset_index()
    daily_data = resC.copy()
    resC.append = 0
    resC['prev_sales'] = resC['Quantity'].shift(1) #name
    resC = resC.dropna()
    resC['diff'] = (resC['Quantity'] - resC['prev_sales']) #name
    df_supervised = resC.drop(['prev_sales'],axis=1)
    for inc in range(1,before_range):
        field_name = 'lag_' + str(inc)
        df_supervised[field_name] = df_supervised['diff'].shift(inc)
    df_supervised = df_supervised.dropna().reset_index(drop=True)

    df_model = df_supervised.drop(['Quantity','date'],axis=1)
    # print(df_model)
    return df_model

def scale_train(train_set,models):
    if models == []:
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaler = scaler.fit(train_set)
    else:
        scaler = pickle.loads(models[0].scope)
    train_set_scaled = scaler.transform(train_set)
    return train_set_scaled,scaler

def convertToTrain(train_set):
    train_set = train_set.reshape(train_set.shape[0], train_set.shape[1])
    X_train, y_train = train_set[:, 1:], train_set[:, 0:1]
    X_train = X_train.reshape(X_train.shape[0],1, X_train.shape[1]) #1 в конце или по центру
    return X_train, y_train
def compile_LSTM_model(shape,params = {}):
    model = km.Sequential()
    if params != {}:
        pass #кастомные параметры через API
    else:
        model.add(kl.LSTM(20,input_shape=(shape[1], shape[2])))
        model.add(kl.Dropout(0.08))
        model.add(kl.Dense(1, activation="elu"))
        model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def trainLSTM(data,models,do_scale = True,epochs = 100,batch = 32,verbose = 0,before_range = 5):
    data = transform_data_train(data,before_range)
    train_set = data.values
    if do_scale:
        train_set, scaler = scale_train(train_set,models)

    X_train, y_train = convertToTrain(train_set if do_scale else np.array(train_set))
    if models == []:
        model = compile_LSTM_model(X_train.shape)
    else:
        model = pickle.loads(models[0].model)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch, verbose=verbose, shuffle=False)
    K.clear_session()
    if do_scale:
        return pickle.dumps(model),pickle.dumps(scaler)
    return pickle.dumps(model),pickle.dumps(scaler)