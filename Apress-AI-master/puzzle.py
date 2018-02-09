
from my_or_tools import newSolver, SolVal
from my_or_tools import k_out_of_n

def get_row(x,i):
    return [x[i][j] for j in range(len(x[0]))]
def get_column(x,i):
    return [x[j][i] for j in range(len(x[0]))]

def solve_maxrook(n):
  s = newSolver('Maxrook',True)
  x = [[s.IntVar(0,1,'') for _ in range(n)] for _ in range(n)]
  for i in range(n):  
    k_out_of_n(s,1,get_row(x,i),'<=')
    k_out_of_n(s,1,get_column(x,i),'<=')
  Count = s.Sum(x[i][j] for i in range(n) for j in range(n)) 
  s.Maximize(Count)
  rc = s.Solve()
  y =[[[' ','R'][int(SolVal(x[i][j]))]\
       for j in range(n)] for i in range(n)]
  return rc,y

def get_se(x,i,j,n):
  return [x[i+k % n][j+k % n] for k in range(n-i-j)]
def get_ne(x,i,j,n):
  return [x[i-k % n][j+k % n] for k in range(i+1-j)]

def solve_maxpiece(n,p):
  s = newSolver('Maxpiece',True)
  x = [[s.IntVar(0,1,'') for _ in range(n)] for _ in range(n)]
  for i in range(n):  
    if p in ['R' ,'Q']:
      k_out_of_n(s,1,get_row(x,i),'<=')
      k_out_of_n(s,1,get_column(x,i),'<=')
    if p in ['B', 'Q']:
      for j in range(n):
        if i in [0,n-1] or j in [0,n-1]:
          k_out_of_n(s,1,get_ne(x,i,j,n),'<=')
          k_out_of_n(s,1,get_se(x,i,j,n),'<=')
  Count = s.Sum(x[i][j] for i in range(n) for j in range(n)) 
  s.Maximize(Count)
  rc = s.Solve()
  y=[[[' ',p]\
     [int(SolVal(x[i][j]))] for j in range(n)] for i in range(n)]
  return rc,y

def get_subgrid(x,i,j):
  return [x[k][l] for k in range(i*3,i*3+3)\
                  for l in range(j*3,j*3+3)]
def all_diff(s,x):
  for k in range(1,len(x[0])):
    s.Add(sum([e[k] for e in x]) <= 1)

def solve_sudoku(G):
  s,n,x = newSolver('Sudoku',True),len(G),[]
  for i in range(n): 
    row=[]
    for j in range(n):
      if G[i][j] == None:
        v=[s.IntVar(1,n+1,'')]+[s.IntVar(0,1,'')\
                                for _ in range(n)]
        s.Add(v[0] == sum(k*v[k] for k in range(1,n+1))) 
      else:
        v=[G[i][j]]+[0 if k!=G[i][j] else 1\
                     for k in range(1,n+1)]
      row.append(v)
    x.append(row) 
  for i in range(n):
    all_diff(s,get_row(x,i))
    all_diff(s,get_column(x,i))
  for i in range(3):
    for j in range(3):
      all_diff(s,get_subgrid(x,i,j))
  rc = s.Solve()
  return rc,[[SolVal(x[i][j][0]) for j in range(n)]\
             for i in range(n)]

def newIntVar(s, lb, ub):
  l=ub-lb+1
  x=[s.IntVar(lb, ub, '')]+[s.IntVar(0,1,'') for _ in range(l)]
  s.Add(1    == sum(         x[k] for k in range(1,l+1)))
  s.Add(x[0] == sum((lb+k-1)*x[k] for k in range(1,l+1)))
  return x
def all_different(s,x):
  lb=min(int(e[0].Lb()) for e in x)
  ub=max(int(e[0].Ub()) for e in x)
  for v in range(lb,ub+1):
    all = []
    for e in x:
      if e[0].Lb() <= v <= e[0].Ub():
        all.append(e[1 + v - int(e[0].Lb())])
    s.Add(sum(all) <= 1)
def neq(s,x,value):
  s.Add(x[1+value-int(x[0].Lb())] == 0)

def solve_smm():
  s = newSolver('Send more money',True)
  ALL = [S,E,N,D,M,O,R,Y] = [newIntVar(s,0,9) for k in range(8)]
  s.Add(              1000*S[0]+100*E[0]+10*N[0]+D[0]
        +             1000*M[0]+100*O[0]+10*R[0]+E[0]
        == 10000*M[0]+1000*O[0]+100*N[0]+10*E[0]+Y[0])
  all_different(s,ALL)
  neq(s,S,0)
  neq(s,M,0)
  rc = s.Solve()
  return rc,SolVal([a[0] for a in ALL])

from my_or_tools import reify, reify_force, reify_raise

def solve_lady_or_tiger():
  s = newSolver('Lady or tiger', True)
  Rooms = range(1,10) 
  R = [None]+[newIntVar(s,0,2) for _ in Rooms]
  S = [None]+[s.IntVar(0,1,'') for _ in Rooms]
  i_empty,i_lady,i_tiger = 1,2,3 
  k_out_of_n(s,1,[R[i][i_lady] for i in Rooms]) 
  for i in Rooms:
    reify_force(s,[1],[R[i][i_tiger]],0,S[i],'<=') 
    reify_raise(s,[1],[R[i][i_lady]],1,S[i],'>=') 
  v=[1]*5
  reify(s,v,[R[i][i_lady] for i in range(1,10,2)],1,S[1],'>=') 
  reify(s,[1],[R[2][i_empty]],1,S[2],'>=') 
  reify(s,[1,-1],[S[5],S[7]],0,S[3],'>=') 
  reify(s,[1],[S[1]],0,S[4],'<=') 
  reify(s,[1,1],[S[2],S[4]],1,S[5],'>=') 
  reify(s,[1],[S[3]],0,S[6],'<=') 
  reify(s,[1],[R[1][i_lady]],0,S[7],'<=') 
  reify(s,[1,1],[R[8][i_tiger],R[9][i_empty]],2,S[8],'>=') 
  reify(s,[1,-1],[R[9][i_tiger],S[6]],1,S[9],'>=') 
  rc = s.Solve()
  return rc,[SolVal(S[i]) for i in Rooms],\
    [SolVal(R[i]) for i in Rooms]
