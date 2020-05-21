import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import keras.layers as kl
import keras.models as km
from keras import backend as K 
import numpy as np
# import matplotlib.pyplot as plt
from scipy.optimize import minimize 
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
import math
import random
import pickle
import time

# import keras.backend.tensorflow_backend as tb
# tb._SYMBOLIC_SCOPE.value = True

# from scipy.optimize import fmin

def trainModelsAndPredict(inData,before_range,model,slen = 0):
    # print(data['Quantity'] != data['Quantity'].min())
    data = pd.DataFrame(columns = {'Quantity','date'})
    # print(type_id)
    for sale in inData:
        # if sale.product_item.product_type_id == type_id: 
        data = data.append({'Quantity':int(sale[1]),'date':sale[0]}, ignore_index=True)
    # for i in inData:
    #     data = data.append({'Quantity':i[-1].count,'date':i[0].date}, ignore_index=True)

    data = data.set_index(['date'])
    # print(type(slen))
    # print(data,len(data))
    # print(data)
    # data = data['Quantity'].resample('D').sum()
    # if slen < len(data):
    #     slen = len(data)//3
    # print(data)
    # slen = len(data[data != min(data)]) 
    # slen = 1 #для теста
    if slen == 0:
        a,b,g = -1,-1,-1
        prediction = 0
    else:
        a,b,g = train(data,slen)
        prediction = predict_rare(data.values,a,b,g,slen)
    # if slen <= (len(data)*7)//10:
    #     a,b,g = train(data,slen)
    # else:
    #     a,b,g = -1,-1,-1
    print(before_range)
    model,scaler,before_range = trainLSTM(data,do_scale = True,epochs = 100,batch = 32,verbose = 0,before_range = before_range,modelI = model)
    print(before_range)
    lstm_pred = int(predict_sales(inData[-(before_range + 1):],before_range = before_range + 1,scaler = scaler,model = model)[0][0])
    return a,b,g,model,scaler,int(prediction[0][0]),before_range,lstm_pred
    
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
        # print(len(self.series),'lenSeries',self.slen)
        n_seasons = int(len(self.series)/self.slen)
        # print(type(self.slen))
        for j in range(n_seasons):
            # print(self.slen*j,self.slen,type(self.slen*j),type(self.slen))
            # print(type(self.series[self.slen*j:self.slen*j+self.slen]))
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
    # print()
    # идем по фолдам, на каждом обучаем модель, строим прогноз на отложенной выборке и считаем ошибку
    # print(len(values))
    # print(tscv)
    for train, test in tscv.split(values):
        # print('lenTrain',len(values[train]))
        # print('lenTest',len(values[test]))
        # print('slen',slen)
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
def scale_train(train_set,model):
    if model == None:
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaler = scaler.fit(train_set)
    else:
        scaler = pickle.loads(model.scope)
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

def trainLSTM(data,modelI,do_scale = True,epochs = 100,batch = 32,verbose = 0,before_range = 5):
    if modelI != None:
        model = pickle.loads(modelI.model)
        if before_range == None:
            before_range = model.layers[0].input_shape[1] + 2
    data = transform_data_train(data,before_range)
    print(data,'train')
    train_set = data.values
    if do_scale:
        train_set, scaler = scale_train(train_set,modelI)

    X_train, y_train = convertToTrain(train_set if do_scale else np.array(train_set))
    if modelI == None:
        model = compile_LSTM_model(X_train.shape)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch, verbose=verbose, shuffle=False)
    K.clear_session()
    if do_scale:
        return pickle.dumps(model),pickle.dumps(scaler),before_range
    return pickle.dumps(model),before_range

def predictWinters(data,alpha_final,beta_final,gamma_final,slen,n_preds,scaling_factor):
    print(data,len(data),'dataWinters')
    model = HoltWinters(data, slen = slen, alpha = alpha_final, beta = beta_final, gamma = gamma_final, n_preds = n_preds,scaling_factor = scaling_factor)
    model.triple_exponential_smoothing()
    return model.result[-n_preds:]

def predict_rare(data,a,b,g,slen,step = False,n_preds = 1,scaling_factor = 2.5):
    if step:
        tres = predictWinters(step,a,b,g,slen,n_preds,scaling_factor)
        return [tres,step[-n_preds:]]
    else:
        res = predictWinters(data,a,b,g,slen,n_preds,scaling_factor)
        return [res]

class Population:

    def __init__(self):
        self.population = []
        self.fronts = []

    def __len__(self):
        return len(self.population)

    def __iter__(self):
        return self.population.__iter__()

    def extend(self, new_individuals):
        self.population.extend(new_individuals)

    def append(self, new_individual):
        self.population.append(new_individual)


class Individual(object):

    def __init__(self):
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        self.features = None
        self.objectives = None

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.features == other.features
        return False

    def dominates(self, other_individual):
        and_condition = True
        or_condition = False
        for first, second in zip(self.objectives, other_individual.objectives):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return (and_condition and or_condition)


class Problem:

    def __init__(self, objectives, num_of_variables, variables_range,extend_vars = 0, expand=True, same_range=False):
        self.num_of_objectives = len(objectives)
        self.num_of_variables = num_of_variables
        self.objectives = objectives
        self.expand = expand
        self.variables_range = []
        if same_range:
            for _ in range(num_of_variables):
                self.variables_range.append(variables_range[0])
        else:
            self.variables_range = variables_range
        self.extend_vars = extend_vars

    def generate_individual(self,sklad,mag,ftrs):
        individual = Individual()
        individual.features = ftrs#[random.randint(*x) for x in self.variables_range]
        individual.features.append(sklad)
        individual.features.append(mag)
        return individual

    def calculate_objectives(self, individual):

                
        if self.expand:
            individual.objectives = [f(*individual.features,self.extend_vars) for f in self.objectives]
        else:
            individual.objectives = [f(individual.features,self.extend_vars) for f in self.objectives]


class NSGA2Utils:

    def __init__(self, problem,mutation_probability, crossover_probability, num_of_individuals=100,num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5):

        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.num_of_tour_particips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.crossover_param = crossover_param
        self.mutation_param = mutation_param
        
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability

    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            for i in self.problem.extend_vars:
                individual = self.problem.generate_individual(i['war'].id,i['shop'].id,[random.randint(*x) for x in self.problem.variables_range])
                self.problem.calculate_objectives(individual)
                population.append(individual)
        return population

    # def create_initial_population(self):
    #     population = Population()
    #     for _ in range(self.num_of_individuals):
    #         for i in self.problem.extend_vars:
    #             individual = self.problem.generate_individual(i['war'].id,i['shop'].id,[random.randint(*x) for x in self.problem.variables_range])
    #             self.problem.calculate_objectives(individual)
    #             population.append(individual)
    #     return population




    def fast_nondominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10**9
                front[solutions_num-1].crowding_distance = 10**9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0: scale = 1
                for i in range(1, solutions_num-1):
                    front[i].crowding_distance += (front[i+1].objectives[m] - front[i-1].objectives[m])/scale

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def create_children(self, population):
        children = []
        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1
            while parent1 == parent2:
                parent2 = self.__tournament(population)
            child1, child2 = self.__crossover(parent1, parent2)
            self.__mutate(child1)
            self.__mutate(child2)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children

    def __crossover(self, individual1, individual2):
        for i in self.problem.extend_vars:
            child1 = self.problem.generate_individual(i['war'].id,i['shop'].id,[random.randint(*x) for x in self.problem.variables_range])
            child2 = self.problem.generate_individual(i['war'].id,i['shop'].id,[random.randint(*x) for x in self.problem.variables_range])
#         if random.uniform(0,1) < self.crossover_probability:
        num_of_features = 2 #len(child1.features)
        genes_indexes = range(num_of_features)
        for i in genes_indexes:
            beta = self.__get_beta()
            x1 = (individual1.features[i] + individual2.features[i])/2
            x2 = abs((individual1.features[i] - individual2.features[i])/2)
            child1.features[i] = x1 + beta*x2
            child2.features[i] = x1 - beta*x2
        return child1, child2

    def __get_beta(self):
        u = random.random()
        if u <= 0.5:
            return (2*u)**(1/(self.crossover_param+1))
        return (2*(1-u))**(-1/(self.crossover_param+1))

    def __mutate(self, child):
#         if random.uniform(0,1) < self.mutation_probability:
        num_of_features = 2#len(child.features)
        for gene in range(num_of_features):
            u, delta = self.__get_delta()
            if u < 0.5:
                child.features[gene] += delta*(child.features[gene] - self.problem.variables_range[gene][0])
            else:
                child.features[gene] += delta*(self.problem.variables_range[gene][1] - child.features[gene])
            if child.features[gene] < self.problem.variables_range[gene][0]:
                child.features[gene] = self.problem.variables_range[gene][0]
            elif child.features[gene] > self.problem.variables_range[gene][1]:
                child.features[gene] = self.problem.variables_range[gene][1]

    def __get_delta(self):
        u = random.random()
        if u < 0.5:
            return u, (2*u)**(1/(self.mutation_param + 1)) - 1
        return u, 1 - (2*(1-u))**(1/(self.mutation_param + 1))

    def __tournament(self, population):
        participants = random.sample(population.population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or (self.crowding_operator(participant, best) == 1 and self.__choose_with_prob(self.tournament_prob)):
                best = participant
        return best

    def __choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        return False


class Evolution:

    def __init__(self, problem, num_of_generations=1000, num_of_individuals=100, num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5,mutation_probability = 0.5, crossover_probability = 0.5):
        self.utils = NSGA2Utils(problem,mutation_probability, crossover_probability, num_of_individuals, num_of_tour_particips, tournament_prob, crossover_param, mutation_param)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals

    def evolve(self):
        self.population = self.utils.create_initial_population()
        for ind in self.population.population:
            print(ind.features,ind.objectives,'pop')
        # print(self.population.population,'pop')
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)
        children = self.utils.create_children(self.population)
        returned_population = None
        for i in range(self.num_of_generations):
            print(i)
            self.population.extend(children)
            self.utils.fast_nondominated_sort(self.population)
            new_population = Population()
            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1
            self.utils.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals-len(new_population)])
            returned_population = self.population
            self.population = new_population
            self.utils.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
            children = self.utils.create_children(self.population)
        return returned_population.fronts[0]



def transform_data(resC,before_range,stepGL = False):
    if stepGL:
        data = pd.DataFrame(columns = {'Quantity','date'})
        # print(stepGL,'stepGL')
        for sale in stepGL:
            data = data.append({'Quantity':sale[1],'date':sale[0]}, ignore_index=True)
        daily_data = data.copy()
        resC = data.reset_index()
        resC.append = 0
        resC['prev_sales'] = resC['Quantity'].shift(-1) #name
        resC = resC.dropna()
        # print(resC)
        resC['diff'] = (resC['Quantity'] - resC['prev_sales']) #name
        # print(resC)
        df_supervised = resC.drop(['prev_sales'],axis=1)
        # print(df_supervised,'step')
        for inc in range(1,before_range-1):
            # print(df_supervised,'super1')
            field_name = 'lag_' + str(inc)
            df_supervised[field_name] = df_supervised['diff'].shift(-inc)
            # print(df_supervised,'super2')
        df_supervised = df_supervised.dropna().reset_index(drop=True)
        step = df_supervised.drop(['Quantity','date','index'],axis=1)
        # print(step,'step_after',len(step))
        return daily_data.loc[0,'Quantity'],step,data.loc[len(data)-len(step):,'Quantity']
    else:
        # before_range -= 2
        # print(resC,'resC')
        # print(before_range)
        # print(resC)
        data = pd.DataFrame(columns = {'Quantity','date'})
        # print(type_id)
        for i in resC:
            # print(i)
            data = data.append({'Quantity':i[1],'date':i[0]}, ignore_index=True)
        # print(data,before_range)
        # print(data)
        resC = data.reset_index()
        daily_data = resC.copy()
        resC.append = 0
        resC['prev_sales'] = resC['Quantity'].shift(-1) #name
        # resC = resC.dropna()
        # print(resC)
        resC['diff'] = (resC['Quantity'] - resC['prev_sales']) #name
        # print(resC)
        df_supervised = resC.drop(['prev_sales'],axis=1)
        # print(df_supervised)
        for inc in range(1,before_range-1):
            # print(df_supervised,'super1')
            field_name = 'lag_' + str(inc)
            df_supervised[field_name] = df_supervised['diff'].shift(-inc)
            # print(df_supervised,'super2')
        df_supervised = df_supervised.dropna().reset_index(drop=True)
        df_model = df_supervised.drop(['Quantity','date','index'],axis=1)
        # print(df_model,'df_model')
        # print(daily_data.loc[len(daily_data)-1,'Quantity'])
        # only_lag = df_model[-before_range:]
    #     print(daily_data.values[-2-step:-1,1])
        # print(daily_data)
        return df_model,daily_data.loc[0,'Quantity']

#!!!!!!!!!!!!!!!!!!!model.layers[0].input_shape[1]!!!!!!!!!!!!!!!!!!

# def scale_trainPR(train_set):
#     scaler = MinMaxScaler(feature_range=(-1, 1))
#     scaler = scaler.fit(train_set)
    
#     train_set_scaled = scaler.transform(train_set)
# #     train_set_scaled = train_set_scaled.reshape(train_set_scaled.shape[0], train_set_scaled.shape[1])
#     return train_set_scaled,scaler #test_set

def scale_test(test_set,scaler):
    test_set = scaler.transform(test_set)
    return test_set



def convertToPred(pred_set):
#     pred_set = np.array(pred_set)
    pred_set = pred_set.reshape(pred_set.shape[0], pred_set.shape[1])
    X_test = pred_set[:]
    X_test = X_test.reshape(X_test.shape[0],1, X_test.shape[1])
    return X_test
def convertToTest(test_set):
#     test_set = np.array(test_set)
    test_set = test_set.reshape(test_set.shape[0], test_set.shape[1])
    X_test = test_set[:, 1:]
    X_test = X_test.reshape(X_test.shape[0],1, X_test.shape[1]) #1 в конце или по центру
    return X_test
def convertToTrain(train_set):
#     train_set = np.array(train_set)
    train_set = train_set.reshape(train_set.shape[0], train_set.shape[1])
    X_train, y_train = train_set[:, 1:], train_set[:, 0:1]
    X_train = X_train.reshape(X_train.shape[0],1, X_train.shape[1]) #1 в конце или по центру
    return X_train, y_train

# def prepare_answer(y_pred, X_test):
#     y_pred = y_pred.reshape(y_pred.shape[0], 1, y_pred.shape[1])
#     pred_test_set = []
#     for index in range(0,len(y_pred)):
# #         print(np.concatenate([y_pred[index],X_test[index]],axis=1))
#         pred_test_set.append(np.concatenate([y_pred[index],X_test[index]],axis=1))
#     pred_test_set = np.array(pred_test_set)
#     pred_test_set = pred_test_set.reshape(pred_test_set.shape[0], pred_test_set.shape[2])
#     return pred_test_set

def shift(resC,before_range):
    # print(resC)
    resC.loc[len(resC)] = 0
    resC = resC.dropna()
    # print(before_range)
    for inc in range(1,before_range-1):
        field_name = 'lag_' + str(inc)
        resC[field_name] = resC['diff'].shift(inc)
        # print(resC)
    resC = resC.dropna().reset_index(drop=True)
    return resC

def predict_next_day(X_test,model,batch):
    test_set = [[[X_test[0][0][1:]]]]
    diff = model.predict(test_set,batch_size=batch)
    
    return np.concatenate((diff.ravel(),X_test[0][0][1:].ravel()), axis=None)
    
    
def get_quantity(last_quantity,only_lag):
    quantity = []
    for i in only_lag:
        last_quantity = last_quantity + i
        quantity.append(last_quantity)
    return quantity
    

    
def predict_sales(data,scaler,model,step = False,predict_range = 1,do_scale = True,batch = 32,before_range = 5):
    # print(data,'data')
    if step:
        last_quantity,step,stepQ = transform_data(data,before_range,step)
    else:
        only_lag,last_quantity = transform_data(data,before_range)
    scaler,model = pickle.loads(scaler),pickle.loads(model)
    # print(only_lag,'lag')
    # print(last_quantity,'lq')
    
#     print(data[0:-1])
#     print(data.loc[len(data)-1],data[-1-step:-1])
    # print(only_lag.values,'vls')
    if step.__class__.__name__ == 'bool':
        pred_set = only_lag.values
    # print(only_lag)
    # train_set = data[0:-1].values
    # print(only_lag)
    if step.__class__.__name__ != 'bool':
        # print(step,'step')
        # print('step')
        test_set = step.values

    if do_scale:
        # train_set, scaler = scale_train(train_set)
        if step.__class__.__name__ == 'bool':
            pred_set = scale_test(pred_set,scaler)
        # print(step.__class__.__name__,step.__class__.__name__ != 'bool')
        # print(step,'step')
        # print('step')
        if step.__class__.__name__ != 'bool':
            # print(step.__class__.__name__,step.__class__.__name__ != 'bool')
            # print(step,'step')
            # print('step')
            test_set = scale_test(test_set,scaler)
            
#     print(train_set)
    # X_train, y_train = convertToTrain(train_set if do_scale else np.array(train_set))
#     print(X_train)
    if step.__class__.__name__ == 'bool':
        X_pred = convertToPred(pred_set if do_scale else np.array(pred_set))
    else:#if step.__class__.__name__ != 'bool':
        X_test = convertToTest(test_set if do_scale else np.array(test_set))
        
    # model = compile_LSTM_model(X_train.shape)
    # model.fit(X_train, y_train, epochs=epochs, batch_size=batch, verbose=verbose, shuffle=False)
#     for layer in model.layers[0]:
#     print(model.layers[0].output_shape,model.layers[0].input_shape[1])
#     print(model.summary())
    # print(only_lag)
    if predict_range > 1 and step.__class__.__name__ == 'bool':
        for i in range(predict_range):
            res = predict_next_day(X_pred,model,batch)
            # print(res)
            if do_scale:
                res = scaler.inverse_transform([res])[0]
    #             print(res)
            only_lag.loc[len(only_lag)] = res
            # print(only_lag,'lag')
            to_train = shift(only_lag,before_range)
            # print(to_train,'to_train')
            pred_set = np.array(to_train.loc[len(to_train)-1].values)
            if do_scale:
                pred_set = scale_test([pred_set],scaler)
    #             print(pred_set)
                X_pred = convertToPred(np.array(pred_set))
            else:
                X_pred = convertToPred(np.array([pred_set]))
        only_lag = only_lag[-predict_range-1:-1]
        quantity = get_quantity(last_quantity,only_lag['diff'])
    else:
        if step.__class__.__name__ == 'bool':
            res = predict_next_day(X_pred,model,batch)
            if do_scale:
                res = scaler.inverse_transform([res])[0]
            # print(res)
            # only_lag.loc[len(only_lag)] = res
            # print(only_lag,'lag')
            # to_train = shift(only_lag,before_range)
            # print(to_train,'to_train')
            # only_lag = only_lag[-predict_range-1:-1]

            only_lag = res

            quantity = get_quantity(last_quantity,[only_lag[0]])
    # print(quantity)

    if step.__class__.__name__ != 'bool':
        # print(X_test)
        prediction = model.predict(X_test,batch_size=batch)
        # print(prediction)
        prediciton = prediction.ravel()
        res = []
        for j in range(len(prediction)):
            rng = [0 for i in range(before_range-1)]
            rng[-1] = prediction[j].tolist()[0]
            res.append(rng)
        # print(res)
        if do_scale:
            for i in range(len(res)):
                res[i] = scaler.inverse_transform([res[i]])[0][-1]
            # prediction = scaler.inverse_transform(res)
            # prediction = [row[-1] for row in res]
#             print(prediction)
        else:
#             prediciton = [i.tolist() for i in prediction]
            res = prediciton.ravel().tolist()
        # print(res,'resInv')
        test_quantity = get_quantity(int(stepQ.values[-1]),prediction)
        # print(test_quantity,stepQ.values)
#         print(type(full_test_quantity_y[0]),type(prediction))
#         print(full_test_quantity_y[1:],test_quantity)
        K.clear_session()
        # print(test_quantity,stepQ.values,'res')
        return [test_quantity, stepQ.values]
    K.clear_session()
    return [quantity]






















alpha = 0.5
price = 10
result = []

def funcE(X):
    res = 0
    for i in X:
        res+=(i/len(X))
    return res

def predictSpros(Fdata,time):
    return int(np.mean([i*random.randint(0,20) for i in Fdata]))

def CheckSendCount(sendCount,minOstat,capacity,pred,zapoln):
    c1 = sendCount>=0
    upperSendCount = minOstat + alpha*(capacity-minOstat) + pred - zapoln
    lowerSendCount = minOstat  + pred - zapoln
    c2 = sendCount <= upperSendCount and sendCount >= lowerSendCount
    return c1 and c2
def CheckZakupkaCount(ZNSC,minOstat,capacity,predSum,zapoln):
    c1 = ZNSC>=0
    upperZNSC = minOstat + alpha*(capacity-minOstat) + predSum - zapoln
    lowerZNSC = minOstat  + predSum - zapoln
    c2 = ZNSC <= upperZNSC and ZNSC >= lowerZNSC
    return c1 and c2
def f1_1(sendCount,skN,magN,extend_vars):
#     skN = math.floor(skN) if skN%1 - 0.5 <= 10**-6 else math.ceil(skN)
#     magN = math.floor(magN) if magN%1 - 0.5 <= 10**-6 else math.ceil(magN)
    minimum = 0
    res = 0
    for i in extend_vars:
        if i['war'].id == int(skN) and i['shop'].id == int(magN):
            # for j in i['shops']:
                # if j[0] == int(magN):
            # before_range = i['before_range']
            # data = i['sales']
            # # steps = i['steps']
            # slen = i['slen']
            # if i['model'].alpha == 0:#-1
            #     scaler = i['model'].scope
            #     model = i['model'].model
            #     spros = float(predict_sales(data, epochs = 1,before_range = before_range,scaler = scaler,model = model)[0][0])
            # else:
            #     spros = i['model'].prediction #predict_rare(data,i['model'].alpha,i['model'].beta,i['model'].gamma,slen)
            spros = i['spros']
            if CheckSendCount(sendCount,i['shop'].minimum,i['shop'].capacity,spros,i['shop'].fullness): #i['shop'].minimum
                res+=price*min(spros,(i['shop'].fullness+sendCount)) #pop[i['sklad']][j[0]][1])
                # result.append([j[0],res])
#     print(res)
    return res
def funcEMin(X):
    res = 0
    for i in X:
        res+=(i/len(X))
    return res
def f2_1(sendCount,skN,magN,extend_vars):
#     skN = math.floor(skN) if skN%1 - 0.5 <= 10**-6 else math.ceil(skN)
#     magN = math.floor(magN) if magN%1 - 0.5 <= 10**-6 else math.ceil(magN)
    res = 0
    minimum = 0

    for i in extend_vars:
        if i['war'].id == int(skN) and i['shop'].id == int(magN):
            # for j in i['shops']:
            #     if j[0] == int(magN):
            # before_range = i['before_range']
            # data = i['sales']
            # steps = i['steps']
            # slen = i['slen']
            spros,listForvector,realSpros = i['spros'],i['listForvector'],i['realSpros']

            if CheckSendCount(sendCount,i['shop'].minimum,i['shop'].capacity,spros,i['shop'].fullness): #i['shop'].minimum
                RNDVector = [(listForvector[gg] - realSpros[gg])/realSpros[gg] if realSpros[gg]!=0 else 0 for gg in range(len(realSpros))]
                res += (-1*funcE(np.minimum([0],[sendCount+i['shop'].fullness - (1+randomVector)*spros-i['shop'].minimum  for randomVector in RNDVector])))+(funcE(np.maximum([0],[sendCount+i['shop'].fullness - (1+randomVector)*spros-i['shop'].capacity  for randomVector in RNDVector])))
                # result.append([j[0],res])
    return res
def f2_2(send,extend_vars):
#     skN,magN = send[2],send[3]
#     skN = math.floor(skN) if skN%1 - 0.5 <= 10**-6 else math.ceil(skN)
#     magN = math.floor(magN) if magN%1 - 0.5 <= 10**-6 else math.ceil(magN)
    res = 0
    minimum = 0# i['shop'].minimum
    # print(extend_vars[0]['sales'])
    # for i in extend_vars[0]['sales']:
    #     print(i,'sales')
    for i in extend_vars:
        if i['war'].id == send[2]:
            skladSumCount = 0
            predSum = 0
            for j in extend_vars:
                if j['shop'].id == int(send[3]):
                    # before_range = j['before_range']
                    # # print(before_range)
                    # data = j['sales']
                    # # print('dddd')
                    # # print(data)
                    # # print(data,'f22')
                    # # steps = i['steps']
                    # slen = j['slen']
                    # # print(slen)
                    # if j['model'].alpha == 0:
                    #     scaler = j['model'].scope
                    #     model = j['model'].model
                    #     spros = float(predict_sales(data, epochs = 1,before_range = before_range,scaler = scaler,model = model)[0][0])
                    # else:
                    #     spros = j['model'].prediction#predict_rare(data,j['model'].alpha,j['model'].beta,j['model'].gamma,slen)
                    spros = i['spros']

                    if CheckSendCount(send[1],i['shop'].minimum,j['shop'].capacity,spros,j['shop'].fullness):
                        skladSumCount += send[1]
                        predSum += spros
        #                 result.append([i,j,predSum,skladSumCount])
            if CheckZakupkaCount(send[0],i['shop'].minimum,i['war'].capacity,predSum,i['war'].fullness): #i['war'].minimum
                res += -min(0,(i['war'].fullness + send[0] - skladSumCount - i['shop'].minimum)) + max(0,(i['war'].fullness + send[0] - skladSumCount - i['war'].capacity))
                # result.append([i['sklad'],res])
    return res

def f2(send,extend_vars):
    # print(extend_vars,'f2')
    # for i in extend_vars[0]['sales']:
        # print(i,'f2sales')
    res = f2_2(send,extend_vars) + f2_1(send[1],send[2],send[3],extend_vars)
#     print(res,'inf2')
    return res
def f1(send,extend_vars):
    # print(extend_vars,'f1')
    res = f1_1(send[1],send[2],send[3],extend_vars)
#     print(res,'inf1')
    return -res








def main_prediction(full):
    # print(full)
    start = time.time()
    print('start')
    problem = Problem(num_of_variables=2, objectives=[f1, f2], variables_range=[(0, 1000),(0, 1000)],expand = False,extend_vars = full)
    evo = Evolution(problem,mutation_param=8,num_of_generations = 100,num_of_individuals = 100,tournament_prob = 0.8,crossover_param = 9,crossover_probability = 0.9,mutation_probability = 0.25)
    func = [[i.objectives,i.features] for i in evo.evolve()]
    print(func,time.time() - start)
    return func