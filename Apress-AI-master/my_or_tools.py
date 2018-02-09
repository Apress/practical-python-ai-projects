
from ortools.linear_solver import pywraplp
def newSolver(name,integer=False):
  return pywraplp.Solver(name,\
                         pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING \
                         if integer else \
                         pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

def SolVal(x):
  if type(x) is not list:
    return 0 if x is None \
      else x if isinstance(x,(int,float)) \
           else x.SolutionValue() if x.Integer() is False \
                else int(x.SolutionValue())
  elif type(x) is list:
    return [SolVal(e) for e in x]

def ObjVal(x):
  return x.Objective().Value()

def pairs(tuple, accum=[]):
  if len(tuple)==0:
    return accum
  else:
    accum.extend((tuple[0],e) for e in tuple[1:])
    return pairs(tuple[1:],accum)

from my_or_tools import ObjVal, SolVal, newSolver

def k_out_of_n(solver,k,x,rel='=='):
  n = len(x)
  binary = sum(x[i].Lb()==0 for i in range(n)) == n and \
           sum(x[i].Ub()==1 for i in range(n)) == n 
  if binary:
    l = x
  else:
    l = [solver.IntVar(0,1,'') for i in range(n)]
    for i in range(n):
      if x[i].Ub() > 0:
        solver.Add(x[i] <= x[i].Ub()*l[i]) 
      else:
        solver.Add(x[i] >= x[i].Lb()*l[i]) 
  S = sum(l[i] for i in range(n))
  if rel == '==' or rel == '=':
    solver.Add(S == k)
  elif rel == '>=':
    solver.Add(S >= k)
  else:
    solver.Add(S <= k)
  return l

def sosn(solver,k,x,rel='<='):
  def sosnrecur(solver,k,l):
    n = len(l)
    d = [solver.IntVar(0,1,'') for _ in range(n-1)]
    for i in range(n):
      solver.Add(l[i] <= sum(d[j] \
        for j in range(max(0,i-1),min(n-2,i+1))))
    solver.Add(k == sum(d[i] for i in range(n-1)))
    return d if k <= 1 else [d,sosnrecur(solver,k-1,d)] 
  n = len(x)
  if 0 < k < n:
    l = k_out_of_n(solver,k,x,rel) 
    return l if k <= 1 else [l,sosnrecur(solver,k-1,l)]

from ortools.linear_solver import pywraplp  
def bounds_on_box(a,x,b):
  Bounds,n = [None,None],len(a)
  s = pywraplp.Solver('Box',pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
  xx = [s.NumVar(x[i].Lb(), x[i].Ub(),'') for i in range(n)] 
  S = s.Sum([-b]+[a[i]*xx[i] for i in range(n)])
  s.Maximize(S)
  rc = s.Solve()
  Bounds[1] = None if rc != 0 else ObjVal(s)
  s.Minimize(S)
  s.Solve()
  Bounds[0] = None if rc != 0 else ObjVal(s)
  return Bounds

def reify_force(s,a,x,b,delta=None,rel='<=',bnds=None):
  # delta == 1 ---> a*x <= b
  n = len(a)
  if delta is None:
    delta = s.IntVar(0,1,'') 
  if bnds is None:
    bnds = bounds_on_box(a,x,b)
  if rel in ['<=','==']:
    s.Add(sum(a[i]*x[i] for i in range(n))<=b+bnds[1]*(1-delta))
  if rel in ['>=','==']:
    s.Add(sum(a[i]*x[i] for i in range(n))>=b+bnds[0]*(1-delta))
  return delta

def reify_raise(s,a,x,b,delta=None,rel='<=',bnds=None,eps=1):
  # a*x <= b ---> delta == 1
  n = len(a)
  if delta is None:
    delta = s.IntVar(0,1,'')
  if bnds is None:
    bnds = bounds_on_box(a,x,b)
  if rel == '<=':
    s.Add(sum(a[i]*x[i] for i in range(n)) \
          >= b+bnds[0]*delta+eps*(1-delta))
  if rel == '>=':
    s.Add(sum(a[i]*x[i] for i in range(n)) \
          <= b+bnds[1]*delta-eps*(1-delta))
  elif rel == '==':
    gm = [s.IntVar(0,1,'') for _ in range(2)]
    s.Add(sum(a[i]*x[i] for i in range(n)) \
          >= b+bnds[0]*gm[0]+eps*(1-gm[0]))
    s.Add(sum(a[i]*x[i] for i in range(n)) \
          <= b+bnds[1]*gm[1]-eps*(1-gm[1]))
    s.Add(gm[0] + gm[1] - 1 == delta)
  return delta

def reify(s,a,x,b,d=None,rel='<=',bs=None,eps=1):
  # d == 1 <---> a*x <= b
  return reify_raise(s,a,x,b,reify_force(s,a,x,b,d,rel,bs),rel,bs,eps)

def maximax(s,a,x,b):
  n = len(a)
  d = [bounds_on_box(a[i],x,b[i]) for i in range(n)]
  zbound = [min(d[i][0] for i in range(n)), max(d[i][1] \
           for i in range(n))]
  z = s.NumVar(zbound[0],zbound[1],'')
  delta = [reify(s,a[i]+[-1],x+[z],b[i],None,'==') \
          for i in range(n)]
  k_out_of_n(s,1,delta)
  s.Maximize(z)
  return z,delta
