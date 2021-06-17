import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize, NonlinearConstraint

def f(x1,x2):
    return (10*(x2-x1**2)**2+(1-x1)**2)

xgrid=np.linspace(-2,2,200)
ygrid=np.linspace(-2,2,200)
xygrid=np.meshgrid(xgrid,ygrid)
XY=f(xygrid[0],xygrid[1])
levels=np.linspace(np.min(XY),np.max(XY),50)
plt.figure(1,figsize=[10,10])
plt.contour(xygrid[0],xygrid[1],XY,levels=levels)
plt.show()

###sympy

x1,x2,f, p1, p2= sp.symbols('x1 x2 f p1 p2')
X=sp.Matrix([x1,x2])
P=sp.Matrix([p1,p2])
f=sp.Matrix([(10*(x2-x1**2)**2+(1-x1)**2)])
df = sp.Matrix(sp.diff(f,X))
B  = sp.hessian(f,X)

fval  = np.array(f.subs([(x1,0),(x2,-1)]))[0]
dfval = np.array(df.subs([(x1,0),(x2,-1)]))
Bval  = np.array(B.subs([(x1,0),(x2,-1)]))

mktest = fval+dfval.T.dot(P) + 0.5* sp.Matrix(Bval.dot(P)).dot(P)
mk_func1=sp.lambdify((p1,p2),mktest)
def mk_func(P):
    return mk_func1(P[0],P[1])[0][0]

XY=mk_func(xygrid)
levels=np.linspace(np.min(XY),np.max(XY),20)
fig,ax = plt.subplots()
fig.set_size_inches(10,10)
plt.contour(xygrid[0],xygrid[1],XY,levels=levels)

deltaAll=[0.2,0.6,1,1.5,2]
for delta in deltaAll:
    def nonlin(X):
        return (X[0]**2+(X[1]+1)**2)**0.5
    constraint=NonlinearConstraint(nonlin,0,delta)
    pmin=minimize(mk_func,[0,-1],constraints=constraint)

    circ=plt.Circle((0,-1),delta)
    ax.add_artist(circ)
    plt.plot([0,pmin.x[0]],[-1,pmin.x[1]],linewidth=2)
plt.show()

fval  = np.array(f.subs([(x1,0),(x2,0.5)]))[0]
dfval = np.array(df.subs([(x1,0),(x2,0.5)]))
Bval  = np.array(B.subs([(x1,0),(x2,0.5)]))

mktest = fval+dfval.T.dot(P) + 0.5* sp.Matrix(Bval.dot(P)).dot(P)
mk_func1=sp.lambdify((p1,p2),mktest)
def mk_func(P):
    return mk_func1(P[0],P[1])[0][0]

XY=mk_func(xygrid)
levels=np.linspace(np.min(XY),np.max(XY),20)
fig,ax = plt.subplots()
fig.set_size_inches(10,10)
plt.contour(xygrid[0],xygrid[1],XY,levels=levels)

deltaAll=[0.2,0.6,1,1.5,2]
for delta in deltaAll:
    def nonlin(X):
        return (X[0]**2+(X[1]-0.5)**2)**0.5
    constraint=NonlinearConstraint(nonlin,0,delta)
    pmin=minimize(mk_func,[0,0.5],constraints=constraint)

    circ=plt.Circle((0,0.5),delta)
    ax.add_artist(circ)
    plt.plot([0,pmin.x[0]],[0.5,pmin.x[1]],linewidth=2)
plt.show()