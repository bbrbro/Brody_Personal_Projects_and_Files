import numpy as np
import tkinter as tk
import csv

names=np.array(['Date','Value'])
a=np.array([['12-01-2018','12-02-2018','12-03-2018'],[4,5,6]])

csv.register_dialect('PIdataDialect',delimiter=',',quoting=csv.QUOTE_NONE)

filer=open('examplePIdata.csv','r')
filew=open('examplePIdata.csv','w')

with filew:
    writer=csv.DictWriter(filew,fieldnames=names)
    writer.writeheader()
    for i in range(0,len(a[:,0])+1):
        writer.writerow({names[0]:a[0,i],names[1]:a[1,i]})


with filer as PIdata:
    reader = csv.DictReader(PIdata,dialect='PIdataDialect')
    for row in reader:
        print(row['Value'])
######################################################

import win32com.client      
  
conn = win32com.client.Dispatch(r'ADODB.Connection')      
DSN = "Provider=PIOLEDB.1;Data Source=Jerome-PI1;Integrated Security=SSPI;Persist Security Info=False"  
conn.Open(DSN)      
  
recordset = win32com.client.Dispatch(r'ADODB.Recordset')      
recordset.Cursorlocation = 3  
recordset.Open("select tag, value from pisnapshot", conn)  
  
if recordset.RecordCount > 0:      
    print("You have a total of {0} tags, and these are their values\n".format( recordset.RecordCount ))     
    print("Tag, Snapshot Value")  
    print("---------------------\n")  
    while not recordset.EOF:  
       source = {field.Name : field.value for field in recordset.Fields}  
       print("{tag}, {value}".format(**source))    
       recordset.MoveNext()  
else:      
    print("There are no tags")     
conn.Close()  

################

import PIconnect as PI
with PI.PIserver() as server:
    points = server.search('*')
    for point in points:
        print(point.name, point.current_value)
        
with PI.PIAFDatabase() as database:
    for child in database.children:
        for attribute in child.attribbues:
            print(attribute.name, attribute.current_value)
            
            
###################
            
import clr
clr.AddReference("OSISoft.PISDK")
clr.AddReference("OSISoft.PISDKCommon")
import PISDK.PISDK
import PISDKCommon

sdk = PISDK.PISDKClass()
srv = sdk.Servers[""]
srv.Open("UID=;PWD="); 
point = srv.PIPoints[""]
async = PISDKCommon.PIAsynchStatusClass()

vals = point.Data.RecordedValues("*-1h","*",PISDK.BoundaryTypeConstants.btAuto,"",
                                 PISDK.FilteredViewConstants.fvShowFilteredState,async)
for val in vals:
    print "%s : %s" % (val.TimeStamp.LocalDate.ToString(),val.Value)


########################



import time
from datetime import datetime, timedelta
from win32com.client import Dispatch
tdMax = timedelta(minutes=15)
pisdk = Dispatch('PISDK.PISDK')
myServer = pisdk.Servers('PI_ServerName')
con =Dispatch('PISDKDlg.Connections')
con.Login(myServer,'username','password',1,0)
piTimeStart = Dispatch('PITimeServer.PITimeFormat')
piTimeEnd = Dispatch('PITimeServer.PITimeFormat')
piTimeStart.InputString = '08-25-2009 00:00:00'
piTimeEnd.InputString = '08-25-2009 23:59:59'
sampleAsynchStatus = Dispatch('PISDKCommon.PIAsynchStatus')
samplePoint = myServer.PIPoints['tagname']
sampleValues = samplePoint.Data.Summaries2(piTimeStart,piTimeEnd,'1h',5,0,sampleAsynchStatus)
t0 = datetime.now()
while True:
    try:
        valsum = sampleValues("Average").Value # retrieve the value
        break  # it will get out of infinite loop when there is no error
    except:  # it failed because server needs more time
        td = datetime.now() - t0
        if td > tdMax:
            print "It is taking so long to get PI data ! Exiting now ...."
            exit(1)
        time.sleep(3)
i = 1
while i < valsum.Count+1:
    print valsum(i).Value, valsum(i).ValueAttributes('Percentgood').Value
    i += 1
    
    
###########
    
    
    
#!/usr/bin/python  
# -*- coding: iso-8859-15 -*-  
import os, sys  
import requests  
import logging  
import datetime  
import random  
import json  
import time  
  
  
logging.basicConfig(filename='piwebapi.log',level=logging.INFO)  
  
  
dns = "192.0.0.1"  
pathprefix = "\\\\WIN-X\Database1\WIN-X ModuleDB\Sample1"  
  
  
try:  
  L = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]  
  starttime = datetime.datetime(2013, 11, 30, 0, 0, 0)  
  endtime = datetime.datetime(2014, 11, 25, 0, 0, 0)  
  delta = datetime.timedelta(days=1)  
  newtime = starttime  
  while newtime <= endtime:  
  newtime = newtime + delta  
  #logging.info("******************* Processing for date %s" % (newtime))  
  for i in L:  
  # find the related attribute from result  
  geturl = "https://%s/piwebapi/attributes?path=%s%s|Sample" % (dns, pathprefix, i)  
  response = requests.get(geturl, verify=False)  
  data = response.json()  
  webIdKey = u"WebId"  
  linksKey = u"Links"  
  if response.status_code == 200 and data.has_key(webIdKey):  
  webIdAttribute = data[webIdKey]  
  # set a value  
  posturl = ("https://%s/piwebapi/streams/%s/value" % (dns, webIdAttribute))  
  postheaders = {'content-type': 'application/json'}  
  postbody = json.dumps({  
  u"Timestamp": (u"%s" % newtime.isoformat()),  
  u"Value": ("%s" % random.randint(10, 45)),  
  #u"UnitsAbbreviation": "°C",  
  u"Good": u"true",  
  u"Questionable": u"false",  
  })  
  postparam = {'updateOption':'Replace', 'bufferOption':'DoNotBuffer'}  
  responsepost = requests.post(url=posturl, verify=False, data=postbody, headers=postheaders, params=postparam)  
  logstr = "posturl:%s statusget: %s, body: %s, statuspost: %s, response.json()" % (responsepost.url, response.status_code, postbody, responsepost.status_code)  
  if(200<=responsepost.status_code<300):  
  logging.debug(logstr)  
  else:  
  logging.error(logstr)  
  else:   
  logging.error("status: %s, WebId NOT FOUND, json:%s" % (response.status_code, data))  
  pass  
  #time.sleep(2)  
except Exception, e:  
  logging.error("error during procssing %s" %(e))  
  raise  
finally:  
  pass  