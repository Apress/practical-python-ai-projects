
from ortools.linear_solver import pywraplp                                
def solve_coexistence():
  t = 'Amphibian coexistence'
  s = pywraplp.Solver(t,pywraplp.Solver.GLOP_LINEAR_PROGRAMMING) 
  x = [s.NumVar(0, 1000,'x[%i]' % i) for i in range(3)]       
  pop = s.NumVar(0,3000,'pop') 
  s.Add(2*x[0] + x[1] + x[2] <= 1500)                           
  s.Add(x[0] + 3*x[1] + 2*x[2] <= 3000)                          
  s.Add(x[0] + 2*x[1] + 3*x[2] <= 4000)                          
  s.Add(pop == x[0] + x[1] + x[2]) 
  s.Maximize(pop)                                
  s.Solve() 
  return pop.SolutionValue(),[e.SolutionValue() for e in x]
