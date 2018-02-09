
from random import randint
def gen_data(n,convex=True):
    R=[]
    SQ,SP,TP=0,20,0
    for i in range(n):
        Q = randint(100,200)
        P = randint(1,5)
        if convex:
            SP1 = SP+P
        else:
            SP1 = SP-P
        RR=[SQ, SQ+Q,SP1, TP, TP+Q*(SP1)]
        R.append(RR)
        TP=TP+Q*(SP1)
        SQ=SQ+Q
        SP=SP1
    B = randint(R[0][0],R[n-1][1])
    return R,B

from my_or_tools import ObjVal, SolVal, newSolver

def minimize_piecewise_linear_convex(Points,B):
    s,n = newSolver('Piecewise'),len(Points)
    x = s.NumVar(Points[0][0],Points[n-1][0],'x')
    l = [s.NumVar(0.0,1,'l[%i]' % (i,)) for i in range(n)]  
    s.Add(1 == sum(l[i] for i in range(n)))               
    s.Add(x == sum(l[i]*Points[i][0] for i in range(n)))  
    s.Add(x >= B)                                                 
    Cost = s.Sum(l[i]*Points[i][1] for i in range(n))     
    s.Minimize(Cost)
    s.Solve()
    R =  [l[i].SolutionValue() for i in range(n)]
    return R

def minimize_non_linear(my_function,left,right,precision):
  n = 5
  while right-left > precision:
    dta = (right - left)/(n-1.0)                          
    points = [(left+dta*i, my_function(left+dta*i)) for i in range(n)]  
    G = minimize_piecewise_linear_convex(points,left)
    x = sum([G[i]*points[i][0] for i in range(n)])
    left = points[max(0,[i-1 for i in range(n) \
                         if G[i]>0][0])][0]  
    right = points[min(n-1,[i+1 for i in range(n-1,0,-1) \
                            if G[i]>0][0])][0] 
  return x.SolutionValue()

def verbose_minimize_non_linear(my_function,left,right,precision):
  n,T,iter = 5,[],0
  while right-left > precision:
    delta = (right - left)/(n-1.0)
    points = [(left+delta*i, my_function(left+delta*i)) for i in range(n)]
    T.append([points[i][0] for i in range(n)])
    T.append([points[i][1] for i in range(n)])
    G = minimize_piecewise_linear_convex(points,left)
    x = sum([G[i]*points[i][0] for i in range(n)])
    y = my_function(x)
    G.append(x)
    G.append(y)
    T.append(G)
    left = points[max(0,[i-1 for i in range(n) if G[i]>0][0])][0]
    right = points[min(n-1,[i+1 for i in range(n-1,0,-1) if G[i]>0][0])][0]
    iter = iter+1
    if iter > 10:
        break
  return T
