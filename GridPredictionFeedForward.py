import numpy as np
import pandas as pd
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
import pickle
from os.path import exists
from noaa_sdk import noaa
import datetime
import math
import requests
import json
from datetime import datetime,timedelta
from collections import OrderedDict
import os
import multiprocessing
from joblib import Parallel, delayed
import urllib
import zipfile
import glob

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
        self.start = kwargs.get('start',100000)
    '''
    def __repr__(self):
        return str(self.series)
    '''

    def Raw(self, ser, start):
        # Construct url
        url = 'http://api.eia.gov/series/?api_key=' + self.token + '&series_id=' + ser.upper() + '&start=' + str(start)

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

def FullRefresh(NAMES):
    data_df=pd.DataFrame(columns=['Ticker','Time','Data'])
    for name in NAMES:    
        print(name)
        data = EIAgov(tok, [name])
        hold=data.GetData()
        data_df=data_df.append({'Ticker':name,'Time':hold['Date'].values,'Data':hold[name].values},ignore_index=True)
    data_df.to_pickle('EIAdataframe') #saves the data frame
    return data_df
    
def MissingRefresh(NAMES):
    #This is what is keeping your data for you right here. Deleting this file will full refresh everything
    data_df=pd.read_pickle('EIAdataframe')
    for name in NAMES:
        print(name)
        if sum(data_df['Ticker']==name)==0:
            data = EIAgov(tok, [name])
            hold=data.GetData()
            data_df=data_df.append({'Ticker':name,'Time':hold['Date'].values,'Data':hold[name].values},ignore_index=True)            
        else:
            index=data_df.index[data_df['Ticker']==name].tolist()
            lasttime=data_df['Time'][int(index[0])][0]
            data = EIAgov(tok, [name],start = lasttime)
            hold=data.GetData()
            data_df.iloc[int(index[0])][1]=np.concatenate((hold['Date'].values,data_df.iloc[int(index[0])][1][1:]))
            data_df.iloc[int(index[0])][2]=np.concatenate((hold[name].values,data_df.iloc[int(index[0])][2][1:]))

    data_df.to_pickle('EIAdataframe')    
    return data_df

def get_noaa_data(url, data_type, header):
    r = requests.get(url,data_type,headers=header)
    return r

def download_save(yyyymm,ii,lengd):
    filename = ['QCLCD' + yyyymm + '.zip']
    file_destination = ['Data\Weather\QCLCD'+ yyyymm +'.zip']
    url = ['http://ncdc.noaa.gov/orders/qclcd/'+ filename]
    fprintf('Downloading %d of %d. %s ', ii, lengd, filename)
    try:
        file = urllib.URLopener()
        file.retrieve(url,file_destination)
        fprintf('Success!\n')
    except IOError:
        fprintf('Failure: Couldnt read the file')

def upzip_file(date):
    zipfile = ['Data\Weather\QCLCD'+date+'.zip']
    directory = ['Data\HistWeather']
    try:
        zip_ref = zipfile.Zipfile(zipfile,'r')
        zip_ref.extractall(directory)
        zip_ref.close()
    except IOerror:
        print("Well the file cant open")






if __name__ == '__main__':
    
    tok = '191fa3be5d1d760a28a4ce8e2a1b4f26'
    NAMESD = ['AVA','AZPS','BANC','BPAT','CHPD','CISO','DOPD','EPE','GCPD','IID','IPCO','LDWP','NEVP','NWMT','PACE','PACW','PGE','PNM','PSCO','PSEI','SCL','TEPC','TIDC','TPWR','WACM','WALC','WAUW']
    NAMESNG = ['AVA','AVRN','AZPS','BANC','BPAT','CHPD','CISO','DEAA','DOPD','EPE','GCPD','GRID','GRIF','GWA','HGMA','IID','IPCO','LDWP','NEVP','NWMT','PACE','PACW','PGE','PNM','PSCO','PSEI','SCL','TEPC','TIDC','TPWR','WACM','WALC','WAUW','WWA']
    NAMESTI = ['AVA','AVRN','AZPS','BANC','BPAT','CHPD','CISO','DEAA','DOPD','EPE','GCPD','GRID','GRIF','GWA','HGMA','IID','IPCO','LDWP','NEVP','NWMT','PACE','PACW','PGE','PNM','PSCO','PSEI','SCL','TEPC','TIDC','TPWR','WACM','WALC','WAUW','WWA']
    NAMES1 = ['EBA.' + x + '-ALL.D.H' for x in NAMESD]
    NAMES2 = ['EBA.' + x + '-ALL.DF.H' for x in NAMESD]
    NAMES3 = ['EBA.' + x + '-ALL.NG.H' for x in NAMESNG]
    NAMES4 = ['EBA.' + x + '-ALL.TI.H' for x in NAMESTI]
    NAMES=np.concatenate((NAMES1,NAMES2,NAMES3,NAMES4))
    #Elec demand costs, might need to seperate the D DF NG TI NAMES since they are different i.e. WWA is in TI but not D
    # .D. is demand, .DF. is day ahead demand forecast, .NG. is net gen, .TI. is total net actual interchange
    
        
    Do_you_want_to_refresh = False
    if __name__ == '__main__':
        #check if dataframe file exists
        if exists('EIAdataframe') and Do_you_want_to_refresh == False:
            print("")
            #data_df=MissingRefresh(NAMES)
        else:       
            data_df=FullRefresh(NAMES)
            
    data_df=pd.read_pickle('EIAdataframe')
    
    #################################################
    #NOAA FORCASTING AND HISTORICAL DATA
    
    
    #if __name__ == '__main__':
    #    n = noaa.NOAA()
    #    observations= n.get_observations('84120','US',start='2017-01-01',end='2018-01-01')
    #    forecast = n.get_forecasts('84120','US')
    
    
    #needs to save off data_frame as well as determine how much of an update is necessary
    #must do this for weather as well
    
        
    
    
    
    #noatok='oAicESXEmbdVGumIHtkGnxbbAMFcesht'
    #creds = dict(token=noatok)
    #
    #
    #dtype='data?datasetid=GHCND&datacatagoryid=TEMP&datacatagoryid=HYDROMETEOR&locationid=ZIP:28801&startdate=2017-05-01&enddate=2017-05-03'
    #dtype='datatypes?datacatagoryid=TEMP&limit=500&offset=700'
    ##dtype='data?datasetid=GHCND&datatypeid=TMAX&datatypeid=TMIN&stationid=GHCND:US1UTSL0031&startdate=2018-01-01&enddate=2018-01-03'
    
    ##global daily summaries from 1763 to 2019
    ##NORMAL_DLY or NORMAL_HLY give 30 years sum of climate data, include high low plus 10,90 percentile
    ##MDTX, MDTN, multi day temp max and min
    #noaurl=('https://www.ncdc.noaa.gov/cdo-web/api/v2/')
    #
    #test=get_noaa_data(noaurl+dtype,'',creds)
    #sub=json.loads(test.text)
    #
    #with open('ELEC.txt') as json_file:
    #    ELECdata = json.dumps(json_file.read())
    ##offset x begins with record number x
    #for i in range(0,25):
    #    print(str(i)+""+sub['results'][i]['name'])
    
    #datatypeid's
    #DLY-TAVG-NORMAL
    #DLY-TAVG-STDDEv
    #DLY-TMAX-NORMAL
    #DLY-TMAX-STDDEv
    #DLY-TMIN-NORMAL
    #DLY-TMIN-STDDEV
    #TOBS - temp at time of observation
            
    months=pd.date_range('2007-05-01','2019-04-01',
                         freq='MS').strftime("%Y%m")
    s=set(months)
    
    curdir= os.path.dirname(__file__)
    ziploc = os.path.join(curdir,'Data','Weather')
    fileloc = os.path.join(curdir,'Data','HistWeather')
    if not exists(ziploc):
        os.mkdir(ziploc)
    if not ~exists(fileloc):
        os.mkdir(fileloc)
        
    zipdates=months.copy()
    unzipdates=months.copy()
    
    replacezips=False
    if replacezips == False:
        existzips = glob.glob(ziploc+'*.zip')
        existzips=[x[5:-4] for x in existzips]
        dne = [x for x in zipdates if x not in s]
        zipdates=dne.copy()
        
    replacefiles=False
    if replacefiles == False:
        existfiles= glob.glob(fileloc+'*.txt')
        existfiles=[x[5:-4] for x in existfiles]
        dne = [x for x in unzipdates if x not in s]
        unzipdates=dne.copy()
     
        
    #QCLCD stands for quality conntrolled local climatological data    
    #parallel for loop
    #num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs = 4, backend="threading")(delayed(download_save)(zipdates(i),i,length(zipdates)) for i in range(1,len(zipdates)))
    Parallel(n_jobs = 4, backend="threading")(delayed(unzip_file)(unzipdates(i)) for i in range(1,len(zipdates)))
        
    #stnlist=[]
    #stnid  =[]
    #stntbl =dict
    #stntbl.WBAN=stnid
    
    #d=dir(r'./Data/Weather/HistWeather/*hourly.txt')
    
    
    
    
    #rather than historical hourly data, maybe just daily data high and low data but still run the simulation in hourly version so that it can predict OATT time.
    #need to feed normal temps, as well as 10th and 90th percentile hourly yearly data
    
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