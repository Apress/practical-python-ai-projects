
def gen_diet_problem(nb_foods=5, nb_nutrients=4):
    from random import randint,uniform
    data = []
    ranges = [10**randint(2,4) for i in range(nb_nutrients)]
    x = [randint(15,25) for i in range(nb_foods)] # this must be feasible
    MinNutrient = [0]*nb_nutrients
    MaxNutrient = [0]*nb_nutrients
    for food in range(nb_foods):
        nutrients = [randint(10,ranges[i]) for i in range(nb_nutrients)]
        minmax = [randint(0,x[food]),randint(x[food],2*x[food])]
        cost = round(100*uniform(0,10))/100
        v = nutrients+minmax+[cost]
        data.append(v)
    for j in range(nb_nutrients):
        b = sum([x[i]*data[i][j] for i in range(nb_foods)])
        MinNutrient[j] = randint(0,b)
        MaxNutrient[j] = randint(b, 2*b)
    data.append(MinNutrient+['','','',''])
    data.append(MaxNutrient+['','','',''])
    return data

from my_or_tools import SolVal, ObjVal, newSolver

def solve_diet(N):
  s = newSolver('Diet')
  nbF,nbN = len(N)-2, len(N[0])-3                          
  FMin,FMax,FCost,NMin,NMax = nbN,nbN+1,nbN+2,nbF,nbF+1                           
  f = [s.NumVar(N[i][FMin], N[i][FMax],'') for i in range(nbF)] 
  for j in range(nbN):                                    
    s.Add(N[NMin][j]<=s.Sum([f[i]*N[i][j] for i in range(nbF)]))
    s.Add(s.Sum([f[i]*N[i][j] for i in range(nbF)])<=N[NMax][j])
  s.Minimize(s.Sum([f[i]*N[i][FCost] for i in range(nbF)]))        
  rc = s.Solve()
  return rc,ObjVal(s),SolVal(f)
