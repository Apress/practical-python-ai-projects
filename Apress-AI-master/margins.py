
from my_or_tools import SolVal,ObjVal,newSolver

def solve_margins_classification(A,B):
  n,ma,mb=len(A[0]),len(A),len(B)
  s = newSolver('Classification')
  ua = [s.NumVar(0,99,'') for _ in range(ma)] 
  la = [s.NumVar(0,99,'') for _ in range(ma)] 
  ub = [s.NumVar(0,99,'') for _ in range(mb)] 
  lb = [s.NumVar(0,99,'') for _ in range(mb)] 
  a = [s.NumVar(-99,99,'') for _ in range(n+1)] 
  e = s.NumVar(-99,99,'')
  for i in range(ma):
    s.Add(0 >= a[n]+1-s.Sum(a[j]*A[i][j] for j in range(n))) 
    s.Add(a[n]==s.Sum(a[j]*A[i][j]-ua[i]+la[i]for j in range(n))) 
    s.Add(e <= ua[i]) 
    s.Add(e <= la[i]) 
  for i in range(mb):
    s.Add(0 >= s.Sum(a[j]*B[i][j] for j in range(n))-a[n]+1 ) 
    s.Add(a[n]==s.Sum(a[j]*B[i][j]-ub[i]+lb[i]for j in range(n))) 
    s.Add(e <= ub[i]) 
    s.Add(e <= lb[i]) 

  s.Maximize(e)
  rc = s.Solve()
  return rc,SolVal(a)
