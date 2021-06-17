# Author Brody Westberg
#2/24/2019 7:35

import numpy as np
import scipy.optimize as opt
import random

#Start with our initial values of operational efficiency. These values are in terms of return, i.e., units/dollars/day in
def PerfOps(Y):
    #Gives some arbitrary operations which doubling spending doesn't double output
    X=np.array([3/365,2.8/365,3.1/365,4/365,5/365])*(Y/1000)**-0.1
    return X
#We need to define a total amount of capital that is allocatable
Capital=4900 #$MM
#Now we need to define the product groups that we are working with and thier boundaries.
LowerBound=[10,20,30,40,50]
UpperBound=[Capital,Capital,Capital,Capital,Capital]
#Now lets determine a time range for this optimization
TimeEnd=600#days


#From here we are missing the optimization equation/function and the market data for the optimization
#Lets assume we have some financial model which predicts future prices of the commodities for the time range given    
def GenerateNewCostFunc():
    
    #This creates a random variable for selling price from 0.5 to 1.5
    C=np.zeros((5,TimeEnd))
    for i in range(5):
        C[i,:]=np.array([0.9+random.random()*0.2 for x in range(TimeEnd)])
    
    #Now we can define in our model some extreme event or probability of some extreme events occuring
    Length_of_event=35#days    
    Prob_Of_Event_Per_Day=np.array([0,0.0005,0.001,0.003,0.01])

    for i in range(5):
        EE=np.array([random.random() for x in range(TimeEnd)])>(1-Prob_Of_Event_Per_Day[i])
        EEDays=EE.copy()
        for j in range(Length_of_event):
            EEDays=EEDays+np.roll(EE,j)
        C[i,:]=(EEDays==0)*C[i,:]
    return C

##############
#Cost=GenerateNewCostFunc()
##############
    
#From here we need to determine the cost function. The overall cost function
#occurs over time so therefore we need to "simulate" the environment for the function to occur
#Since the model is stagnant we only need to sum accross time
def ObjFunc(Y):
    Value=Capital-np.sum(Y)+np.sum(Y*PerfOps(Y)*np.sum(Cost,axis=1))
    return -Value

def CapitalConstraint(Y):
    return -np.sum(Y)+Capital #>=0

cons =  ({'type': 'ineq', 'fun': CapitalConstraint})
Bound=opt.Bounds(LowerBound,UpperBound)

InitialGuess=[1000,1000,1000,1000,1000]
#And we can begin the optimization function (many different forms exist, this is a rather brute force method)
res=opt.minimize(ObjFunc,InitialGuess,bounds=Bound,constraints=cons)
print(res.x)
        
        
        
        