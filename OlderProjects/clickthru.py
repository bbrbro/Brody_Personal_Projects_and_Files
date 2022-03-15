# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 16:17:17 2019

@author: brody
"""

import sys
sys.path.append('C\\:Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')
import clr
clr.AddReference('OSIsoft.AFSDK')

#imports the necessary functions
from OSIsoft.AF import *
from OSIsoft.AF.PI import *
from OSIsoft.AF.Search import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *
from OSIsoft.AF.UnitsOfMeasure import *

#sets up the server
piServers = PIServers()
piServer = piServers.DefaultPIServer;
    
#function which gets the current snapshot of the value
def get_current_time():
    print("Hi")
    ######## does a thing

def get_tag_into(tagname):
    tag= PIPoint.FindPIPoint(piServer,tagname)
    lastData = tag.Snapshot()
    return lastData.Units, lastData.Descriptor

def get_tag_snapshot(tagname):
    tag= PIPoint.FindPIPoint(piServer,tagname)
    lastData = tag.Snapshot()
    return lastData.Value, lastData.Timestamp

#function which gets a recorded amount of time for the data
def get_timed_data(tagname,start,stop,dt):
    timerange = AFTimeRange(start,stop)
    tag= PIPoint.FindPIPoint(piServer,tagname)
    recorded = tag.RecordedValues(timerange, AFBoundaryType.Inside, "", False)
    return recorded.Value, recorded.Timestamp

#interpolated values for some time
def get_interp_data(tagname,start,stop,dt):
    delta = AFTimeSpan.Parse(dt)
    timerange = AFTimeRange(start,stop)
    tag= PIPoint.FindPIPoint(piServer,tagname)
    interpolated = tag.InterpolatedValues(timerange, span, "", False)
    return interpolated.Value, interpolated.Timestamp
    
#summeriesvalues
def get_summary_data(tagname,start,stop,dt):
    delta = AFTimeSpan.Parse(dt)
    timerange = AFTimeRange(start,stop)
    tag= PIPoint.FindPIPoint(piServer,tagname)
    summary = tag.Summaries(timerange, span, AFSummaryTypes.Average, AFCalculationBasis.TimeWeighted, AFTimestampCalculation.Auto)
    return summary.Value, summary.Timestamp

#connect to AF
afServers = PISystems()
afServer = afServers.DefaultPISystem
DB = afServer.Databases.DefaultDatabase

################################################################################################
#################################################################################################
################################################################################################


import csv
import numpy as np
csv.register_dialect('PIdataDialect',delimiter=',',quoting=csv.QUOTE_NONE)

#create csv
def create_csv(tagname):
    info = np.array(['Description','Units', 'Time', 'Value','Comments'])
    data = np.array([[],[],[],[],[]])
    file = open(np.concatenate(tagname,'.csv'),'w')  
    with file:
        writer = csv.DictWriter(file,fieldnames=info)
        writer.writeheader()
        for data_type in range(0,len(data)):
            for data_pt in range(0,len(data[data_type])):
                writer.writerow({info[data_type]:data[data_type][data_pt]})
                
def read_csv(tagname):
    info = np.array(['Description','Units', 'Time', 'Value','Comments'])
    data = np.array([[],[],[],[],[]])
    file = open(np.concatenate(tagname,'.csv'),'r')
    with file:
        reader = csv.DictReader(data,dialect='PIdataDialect')
        rowNumber=0
        for row in reader:
            data[rowNumber]=row[info].Value
            rowNumber += 1
    return data
   
def append_csv_comment(tagname,comment):
    with open(np.concatenate(tagname,'.csv'),'a') as file:
        writer = csv.writer(file)
        writer.write({'Comment':comment})
    
def append_csv_path(tagname,path):
    with open(np.concatenate(tagname,'.csv'),'a') as file:
        writer = csv.writer(file)
        writer.write({'Path':path})

def write_csv_data(tagname,data):
    info = np.array(['Time', 'Value'])
    with open(np.concatenate(tagname,'.csv'),'w') as file:
        writer = csv.DictWriter(file,fieldnames=info)
        for data_type in range(0,2):
            for data_pt in range(0,len(data[data_type])+1):
                writer.writerow({info[data_type]:data[data_type][data_pt]})
                
def update_csv(tagname,**kwargs):
    data=read_csv(tagname)

    replace = kwargs.get('Replace',False)    
    begin = data['Time'][-1]
    end   = get_current_time()
        
    if replace == True:
        begin = kwargs.get('Start',begin)
        
    end   = kwargs.get('Stop',end)
    delta = kwargs.get('Delta','15m')
    
    value,time=get_summary_data(tagname,begin,end,delta)
    time_start_deletion = bisect_left(data[0,:],time[ 0])
    time_end_deletion   = bisect_left(data[0,:],time[-1])
    #cut the segment
    data[0,:] = np.delete(data[0,:], range( time_start_deletion, time_end_deletion ) )
    data[1,:] = np.delete(data[1,:], range( time_start_deletion, time_end_deletion ) )
    #paste the data
    data[0,:] = np.insert(data[0,:], time_start_deletion,  time)
    data[1,:] = np.insert(data[1,:], time_start_deletion, value)
    write_csv_data(tagname,data)
    
#updates the csv's associated with different segments of data    
def update_type(tagname,scale,path,start,stop,delta):
    tagpath=read_tagnames()
    
    #a global refresh will refresh all up to current time for all data, but does not replace data
    if scale == 'global':
        for tags in range(0,len(tagpath[0,:])):
            update_csv(tagname,Delta=delta,Start=start,Stop=stop)
   
    #a local refresh will refresh only those on the current path 
    elif scale == 'local':
        for tags in range(0,len(tagpath[0,:])):
            if path == tagpath[1,tags]:
                update_csv(tagname,Delta=delta,Start=start,Stop=stop)

    #global total refreshes all data for the time frame given
    elif scale == 'global total':
        for tags in range(0,len(tagpath[0,:])):
            update_csv(tagname,Delta=delta,Start=start,Stop=stop,Replace=True)
    
    #local total refreshes only those on the current path for the time frame given
    elif scale == 'local total':
        for tags in range(0,len(tagpath[0,:])):
            if path == tagpath[1,tags]:
                update_csv(tagname,Delta=delta,Start=start,Stop=stop,Replace=True)

                
def write_tagnames(data):
    info = np.array(['Tagname', 'Path'])
    with open(np.concatenate('tagpath.csv'),'w') as file:
        writer = csv.DictWriter(file,fieldnames=info)
        for data_type in range(0,2):
            for data_pt in range(0,len(data[data_type])+1):
                writer.writerow({info[data_type]:data[data_type][data_pt]})
       
def read_tagnames():
    info = np.array(['Tagname', 'Path'])
    data = np.array([[],[]])
    with open(np.concatenate('tagpath.csv'),'r') as file:
        reader = csv.DictReader(data,dialect='PIdataDialect')
        rowNumber=0
        for row in reader:
            data[rowNumber,:]=row.Value
            rowNumber += 1
    return data
    
################################################################################################
#################################################################################################
################################################################################################
## This segment is for movement architecture

def initialize_path():
    path_start=("/")
    return path_start
def level_down(path,change):
    return np.concatenate(path,change)
def level_up(path,change):
    return path.replace(change,'')
#current_path=X
    #need some global variable to define current path
#def read_paths(tagnames):
def create_temp_tagnames(path):
    tagpath=read_tagnames()
    temp_tagnames=np.array([[],[]])
    for tags in range(0,len(tagpath[0,:])):
        if path == tagpath[1,tags]:
                temp_tagnames=np.append(temp_tagnames,tagpath,1) 
    return temp_tagnames

def add_temp_tagname(tagname,temp_tagnames):
    return np.append(temp_tagnames,np.array(tagname,current_path),1) 

def remove_temp_tagname(tagname,temp_tagnames):
    position=temp_tagname[0,:].index(tagname)
    return np.delete(temp_tagnames,position,1) 

def add_tagname(tagname,path):
    data=read_tagnames()
    data=np.append(data,np.array([tagname,path]),1)
    write_tagnames(data)
    
def remove_tagname(tagname,path):
    data=read_tagnames()
    for pair in range(0,len(data[0,:])):
        if data[:,pair]==np.array([[tagname],[path]]):
            data=np.delete(data,pair,1)
            break
    write_tagnames(data)
    
def current_values(tagnames):
    data=np.arrau([])
    for tagname in tagnames:
        data=np.append(data,get_tag_snapshot(tagname))
    return data

def history_values(tagnames,Start,Stop):
    historical = {}
    for tagname in tagnames:    
        historical[tagname]=read_csv(tagname)
    return historical
    

