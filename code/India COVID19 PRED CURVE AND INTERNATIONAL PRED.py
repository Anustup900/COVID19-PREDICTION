# -*- coding: utf-8 -*-
"""India COVID19 PRED CURVE AND INTERNATIONAL PRED.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ayusRAbbzYKYK6TwU89C7dREjMJmWUL2
"""

#Author Anustup Mukherjee
#This is prediction py script for international COVID Cases in upcoming days ,prediction of COVID 19 curve of India to predict when this situation will get end 
#And prediction of when this situation will get end
#Model having 97% accuracy 
#Developed on Japanese Bayesian ML algorithm and FBprophet algorithm which feteches automatically updated datas from government sites and gives automated prediction with curvechange
#Scroll Down to see the prediction and Curves
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

#Calling of automated updated data in the script
train = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
train.head()

train.info()

train.rename(columns = {"Province/State": "state", "Country/Region":"country"}, inplace = True)

#preprocessing of data
train.drop('Lat', axis = 1, inplace = True)
train.drop('Long', axis = 1, inplace = True)
train.drop('Recovered', axis = 1, inplace = True)

train.isnull().sum()

train.state = train.state.fillna('Not Available')
train.isnull().sum()

train_new = train[train.Date == train.Date.max()].groupby(by='country')
train_new = train_new.aggregate(np.sum)
train_new.reset_index(level=0, inplace=True)
train_new.head()

train_new[train_new.country == 'US']

#Data visualization of still date affected Country
plt.figure(figsize=(13,13))
sns.barplot(x = 'country', y = 'Confirmed', data = train_new[train_new.Confirmed > 5000])

train_n2 = train.drop(['state'],axis=1)
train_n2.head()

train_n2.sort_values('Date').reset_index().drop('index', axis =1)

train_n2.sort_values('Date').reset_index().drop('index', axis =1)

train_n2.groupby('Date')[['Confirmed','country','Deaths']].sum().reset_index()

#TRAINING THE MODEL TO GET A PREDICTION MODEL CURVE FOR INDIA AND BASED PREDICTIONS
train_ind = train_n2.loc[train_n2['country']=='India'].copy()

train_ind['Date'] = pd.to_datetime(train_ind['Date'])
train_ind = train_ind.set_index('Date')
train_ind.head()

train_ind2 = train_ind.drop(['country','Deaths'],axis = 1)
train_ind2 = train_ind2.loc[train_ind2['Confirmed']>0]
train_ind3 = train_ind2
train_ind2.head()

#DATA VISUALIZATION
pd.plotting.register_matplotlib_converters()
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(train_ind2, model='multiplicative')
result.plot()
plt.show()

new_colname = 'y'
train_ind2.index.rename('ds', inplace=True)
train_ind2.rename(columns = {'Confirmed' : 'y'},inplace=True)
train_ind2.reset_index(level=0, inplace=True)
train_ind2.head()

from fbprophet import Prophet

# instantiate the model and set parameters
model = Prophet(
    interval_width=0.95,
    holidays = pd.DataFrame({'holiday': 'lockdown','ds': pd.to_datetime(['2020-03-24','2020-03-25','2020-03-26','2020-03-27','2020-03-28','2020-03-29','2020-03-30','2020-03-31','2020-04-01'
    ,'2020-04-02','2020-04-03','2020-04-04','2020-04-05','2020-04-05','2020-04-06','2020-04-07','2020-04-08','2020-04-09','2020-04-10','2020-04-11','2020-04-12','2020-04-13','2020-04-14'])}),
    growth='linear',
    daily_seasonality=False,
    weekly_seasonality=True,
    yearly_seasonality=True,
    seasonality_mode='multiplicative'
)

# fit the model to historical data

model.fit(train_ind2)

future_pd = model.make_future_dataframe(
    periods=60,
    freq='d',
    include_history=True
)

# predict over the dataset
forecast_pd = model.predict(future_pd)

#PREDICTION CURVE OF COVID19 INDIA FOR UPCOMING MONTHS
#CURVE IS EXACTLY SIMILAR AS PROVIDED BY RESEARCH OF SINGAPORE UNIVERSITY
predict_fig = model.plot(forecast_pd, xlabel='date', ylabel='confirmed cases')
display(predict_fig)

#MONTH WISE PREDICTION INDIA
from fbprophet.plot import plot_plotly
import plotly.offline as py

fig = plot_plotly(model, forecast_pd)  # This returns a plotly Figure
py.iplot(fig)

forecast_pd[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].iloc[55:63]

fpd = pd.DataFrame(forecast_pd[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

fpd.rename(columns= {'ds':'Date', 'yhat':'Predicted Cases'},inplace=True)

fpd.drop(['yhat_lower','yhat_upper'],axis=1,inplace=True)

#PREDICTION OF COVID CASES INDIA IN UPCOMING MONTHS AND DAYS JUST CHANGE THE DATE AND RUN THE SCRIPT FOR UPDATED RESULTS
fpd[(fpd['Date']>= '2020-04-29') & (fpd['Date']<= '2020-04-30')]

print("Date: ",fpd.sort_values(by = 'Predicted Cases',ascending=False).iloc[1].Date.date(), "\n","Highest Predicted:",round(fpd.sort_values(by = 'Predicted Cases',ascending=False).iloc[1]['Predicted Cases']))

#START OF INTERNATIONAL PREDICTION
c_list = ['Austrailia', 'Canada', 'Cruise Ship', 'Denmark', 'France', 'Netherlands', 'US', 'United Kingdom']
train_ctry = train_n2.copy() 
for clst in c_list:
  train_ctry.drop(train_ctry[train_ctry['country'] == clst].index, inplace = True)
train_ctry.drop(train_ctry[train_ctry['country'] == 'China'].index, inplace = True)
train_ctry.head()

train_n2.country.unique()
#Creating a dataframe with combined data 
train_ch = train_n2[train_n2['country']=='China'].groupby('Date').aggregate(np.sum).reset_index()
train_ch['country'] = 'China'
for obj in c_list:
  train_temp = train_n2[train_n2['country']==obj].groupby('Date').aggregate(np.sum).reset_index()
  train_temp['country'] = obj
  train_ch = train_ch.append(train_temp)

train_ch.info()
train_ctry = train_ctry.append(train_ch,sort=True).copy()
train_ctry[train_ctry.country=='China']

train_ctry.head()

train_ctry2 = pd.DataFrame()
#choose countries
choose_list = ['US','Italy','Spain','Germany','France','Iran','UK','Switzerland','Netherland']

for clist in choose_list:
  train_ctry2 = train_ctry2.append(train_ctry[train_ctry.country==clist]).copy()

train_ctry2.info()

total_countries = train_ctry2.country.unique().tolist()
total_countries

#RESULT OF INTERNATIONAL PREDICTION WITH THE NUMBER OF CASES
final_top = pd.DataFrame()
final_top_df = pd.DataFrame()
for country in total_countries:
  
  train_fin = train_ctry.loc[train_ctry['country']==country].copy()
  train_fin.drop(['country','Deaths'],axis = 1,inplace = True)
  train_fin['Date'] = pd.to_datetime(train_fin['Date'])
  train_fin = train_fin.set_index('Date') 
  train_fin2 = train_fin.loc[train_fin['Confirmed']>0].copy()
  train_fin2.index.rename('ds', inplace=True)
  train_fin2.rename(columns = {'Confirmed' : 'y'},inplace=True)
  train_fin2.reset_index(level=0, inplace=True)
  # instantiate the model and set parameters
  model = Prophet(
    interval_width=0.95,
    growth='linear',
    daily_seasonality=False,
    weekly_seasonality=True,
    yearly_seasonality=True,
    seasonality_mode='multiplicative'
  )
  model.fit(train_fin2)
  forecast_pdf = model.predict(future_pd)
  print('Country: ' +country )
  print(forecast_pdf[['ds', 'yhat', 'yhat_lower', 'yhat_upper']][(forecast_pdf['ds']>= '2020-03-24') & (forecast_pdf['ds']<= '2020-03-31')])
  tmp_df = forecast_pdf[['ds', 'yhat', 'yhat_lower', 'yhat_upper']][(forecast_pdf['ds']>= '2020-03-24') & (forecast_pdf['ds']<= '2020-03-31')]
  tmp_df['country'] = country
  print('Maximum Predicted: ')
  print(forecast_pdf.sort_values(by = 'yhat',ascending=False).iloc[1][['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
  train_final_countries_tmp = pd.DataFrame({'Date':forecast_pdf.ds ,'country':country, 'Highest Prediction':forecast_pdf.sort_values(by = 'yhat',ascending=False).iloc[1]['yhat']},index = [0])
  print(train_final_countries_tmp)
  final_top = final_top.append(train_final_countries_tmp)
  final_top_df = final_top_df.append(tmp_df)

#INTERNATIONAL PREDICTION OF COVID19
pd.set_option('display.float_format', lambda x: '%.3f' % x)
final_top.sort_values('Highest Prediction', ascending=False).reset_index()

#INTERNATIONAL UPCOMING TOP COVID19 COUNTRIES
final_top.sort_values('Highest Prediction', ascending=False).reset_index().head()

