# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 08:53:08 2019

@author: brody
"""
import json
import numpy as np
import pandas as pd
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
import pickle
from os.path import exists

#This file performs machine learning to utah power prices and 
#relevent weather to predict grid load



#loads all real time load data from OASIS.OATI.Com
#that is not currently downloaded (+1 day back from today to correct changes)
class EIAgov(object):
    def __init__(self, token, series, **kwargs):
        '''
        Purpose:
        Initialise the EIAgov class by requesting:
        - EIA token
        - id code(s) of the series to be downloaded

        Parameters:
        - token: string
        - series: string or list of strings
        '''
        self.token = token
        self.series = series
        self.start = kwargs.get('start',0)
    '''
    def __repr__(self):
        return str(self.series)
    '''

    def Raw(self, ser, start):
        # Construct url
        url = 'http://api.eia.gov/series/?api_key=' + self.token + '&series_id=' + ser.upper() + '&firstrow=' + str(start)

        try:
            # URL request, URL opener, read content
            response = urlopen(url);
            raw_byte = response.read()
            raw_string = str(raw_byte, 'utf-8-sig')
            jso = json.loads(raw_string)
            return jso

        except HTTPError as e:
            print('HTTP error type.')
            print('Error code: ', e.code)

        except URLError as e:
            print('URL type error.')
            print('Reason: ', e.reason)

    def GetData(self):
        # Deal with the date series                       
        date_ = self.Raw(self.series[0], self.start)        
        date_series = date_['series'][0]['data']
        endi = len(date_series) # or len(date_['series'][0]['data'])
        date = []
        for i in range (endi):
            date.append(date_series[i][0])

        # Create dataframe
        df = pd.DataFrame(data=date)
        df.columns = ['Date']

        # Deal with data
        lenj = len(self.series)
        for j in range (lenj):
            data_ = self.Raw(self.series[j], self.start)
            data_series = data_['series'][0]['data']
            data = []
            endk = len(date_series)         
            for k in range (endk):
                data.append(data_series[k][1])
            df[self.series[j]] = data
        
        return df




tok = '191fa3be5d1d760a28a4ce8e2a1b4f26'
NAMES = ['AVA','AZPS','BANC','BPAT','CHPD','CISO','DOPD','EPE','GCPD','IID','IPCO','LDWP','NEVP','NWMT','PACE','PACW','PGE','PNM','PSCO','PSEI','SCL','SRP','TEPC','TIDC','TPWR','WACM','WALC','WAUW']
NAMES = ['EBA.' + x + '-ALL.D.H' for x in NAMES]
#Elec demand costs, might need to seperate the D DF NG TI NAMES since they are different i.e. WWA is in TI but not D
# .D. is demand, .DF. is day ahead demand forecast, .NG. is net gen, .TI. is total net actual interchange

def FullRefresh(NAMES):
    data_df=pd.DataFrame(columns=['Ticker','Time','Data'])
    for name in NAMES:    
        data = EIAgov(tok, [name])
        hold=data.GetData()
        data_df=data_df.append({'Ticker':name,'Time':hold['Date'].values,'Data':hold[name].values},ignore_index=True)
    data_df.to_pickle('EIAdataframe') #saves the data frame
    return data_df
    
def MissingRefresh(NAMES):
    data_df=pd.read_pickle('EIAdataframe')
    
    for name in NAMES:
        if sum(data_df['Ticker']==name)==0:
            data = EIAgov(tok, [name])
            hold=data.GetData()
            data_df=data_df.append({'Ticker':name,'Time':hold['Date'].values,'Data':hold[name].values},ignore_index=True)
        else:
            idx=np.where(df["Ticker"] == name)
            lasttime=data_df['Ticker'][-1]
            
            data = EIAgov(tok, [name],starttime)
            hold=data.GetData()
            data_df=data_df.append({'Ticker':name,'Time':hold['Date'].values,'Data':hold[name].values},ignore_index=True)

    data_df.to_pickle('EIAdataframe')
    
    return data_df
    
Do_you_want_to_refresh = False
if __name__ == '__main__':
    #check if dataframe file exists
    if exists('EIAdataframe') and Do_you_want_to_refresh == False:
        data_df=MissingRefresh(NAMES)

    else:
        data_df=FullRefresh(NAMES)
        

    #find last time
    
    
#needs to save off data_frame as well as determine how much of an update is necessary
#must do this for weather as well
        
#loads all relevant weather data from ___
#that is not currently downloaded (+1 day back from today to correct changes)

#smashes load data together

#smashes weather data together

#"fixes" data for loads

#"fixes" data for weather

#From here they broke data by region or zones

#Now it needs time predictors hour,month,year,dayofweek,isweekend,isholiday
#Needs to convert these to sin waves

#Autocorrelates the load data itself? Peaks occur at 1 day lag and 7 day lag

#Split data set for training and testing
#Train different regression models
#use MAPE to determine fit accuracy


#linear regression
#stepwise linear regression
#ensemble bagged regression tree
#use feed-forward neural network to solve regression problem

#Compare models on test set and train set. Lowest test set MAPE is best

#Look at model fit graphs