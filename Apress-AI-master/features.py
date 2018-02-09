
from random import randint
def inner(a,b):
  s=0
  for i in range(len(a)):
    s += a[i]*b[i]
  return s

def gen_features(n,m):
  # Generating n vectors of m features linearly separable
  a=gen_hyperplane(m)
  A,B,i=[],[],0
  while len(A) < n:
    x=[randint(-10,10) for _ in range(m)]
    if inner(a[0:m],x) < a[m]-1:
      A.append(x)
  while len(B) < n:
    x=[randint(-10,10) for _ in range(m)]
    if inner(a[0:m],x) > a[m]+1:
      B.append(x)
  return A,B,a

def gen_hyperplane(m):
  return [randint(-10,10) for _ in range(m+1)]

from my_or_tools import SolVal,ObjVal,newSolver

def solve_classification(A,B):
  n,ma,mb=len(A[0]),len(A),len(B)
  s = newSolver('Classification')
  ya = [s.NumVar(0,99,'') for _ in range(ma)] 
  yb = [s.NumVar(0,99,'') for _ in range(mb)] 
  a = [s.NumVar(-99,99,'') for _ in range(n+1)] 
  for i in range(ma):
    s.Add(ya[i] >= a[n]+1-s.Sum(a[j]*A[i][j] for j in range(n))) 
  for i in range(mb):
    s.Add(yb[i] >= s.Sum(a[j]*B[i][j] for j in range(n))-a[n]+1 ) 
  Agap = s.Sum(ya[i] for i in range(ma))
  Bgap = s.Sum(yb[i] for i in range(mb))
  s.Minimize(Agap+Bgap)
  rc = s.Solve()
  return rc,ObjVal(s),SolVal(a)
