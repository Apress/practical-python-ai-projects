
from ortools.linear_solver import pywraplp  
from my_or_tools import SolVal, ObjVal
from my_or_tools_c import bounds_on_box,reify_force,reify_raise,reify,sosn
def main():
  # Test force
  bounds = []
  s = pywraplp.Solver('',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  a = [[0,1],[1,0]]
  b = [4,5]
  x = [s.IntVar(0,10,'x[%i]' % i) for i in range(2)]
  bounds,delta,gamma = [],[],[]
  for j in range(len(a)):
    bounds.append(bounds_on_box(a[j],x,b[j]))
    d = reify_force(s,a[j],x,b[j],rel='==')
    delta.append(d)
  s.Maximize(x[0]+x[1])
  rc = s.Solve()
  if rc == 0:
    print(rc==0,ObjVal(s)==20,SolVal(delta)==[0,0],SolVal(x)==[10,10])
  else:
    print(rc)
  s.Add(delta[0] == 1)
  rc = s.Solve()
  if rc == 0:
    print(rc==0,ObjVal(s)==14,SolVal(delta)==[1,0],SolVal(x)==[10,4])
  else:
    print(rc)
  s.Add(delta[1] == 1)
  #s.Add(a[0][0]*x[0]+a[0][1]*x[1] == b[0])
  #s.Add(a[1][0]*x[0]+a[1][1]*x[1] == b[1])
  rc = s.Solve()
  if rc == 0:
    print(rc==0,ObjVal(s)==9,SolVal(delta)==[1,1],SolVal(x)==[5,4])
  else:
    print(rc)

  # Test raise
  s = pywraplp.Solver('',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  a = [[0,1],[1,0]]
  b = [4,5]
  x = [s.IntVar(0,10,'x[%i]' % i) for i in range(2)]
  bounds,delta,gamma = [],[],[]
  for j in range(len(a)):
    bounds.append(bounds_on_box(a[j],x,b[j]))
    d = reify_raise(s,a[j],x,b[j],rel='==')
    delta.append(d)
  s.Minimize(x[0]+x[1]+delta[0]+delta[1])
  rc = s.Solve()
  if rc == 0:
    #print rc,ObjVal(s),SolVal(delta),SolVal(x)
    print(rc==0,ObjVal(s)==0,SolVal(delta)==[0,0],SolVal(x)==[0,0])
  else:
    print(rc)
  s.Add(a[0][0]*x[0]+a[0][1]*x[1] == b[0])
  #s.Add(delta[0] == 1)
  rc = s.Solve()
  if rc == 0:
    #print rc,ObjVal(s),SolVal(delta),SolVal(x)
    print(rc==0,ObjVal(s)==5,SolVal(delta)==[1,0],SolVal(x)==[0,4])
  else:
    print(rc)
  #s.Add(delta[1] == 1)
  s.Add(a[1][0]*x[0]+a[1][1]*x[1] == b[1])
  rc = s.Solve()
  if rc == 0:
    #print rc,ObjVal(s),SolVal(delta),SolVal(x)
    print(rc==0,ObjVal(s)==11,SolVal(delta)==[1,1],SolVal(x)==[5,4])
  else:
    print(rc)


  # Test iff
  s = pywraplp.Solver('',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  a = [[0,1],[1,0]]
  b = [4,5]
  x = [s.IntVar(0,10,'x[%i]' % i) for i in range(2)]
  q = [s.IntVar(0,1,'') for _ in range(2)]
  bounds,delta,gamma = [],[],[]
  for j in range(len(a)):
    bounds.append(bounds_on_box(a[j],x,b[j]))
    d = reify(s,a[j],x,b[j],rel='==')
    delta.append(d)
  s.Minimize(x[0]+x[1])
  sosn(s,1,q,'==')
  rc = s.Solve()
  if rc == 0:
    #print rc,ObjVal(s),SolVal(delta),SolVal(x)
    print(rc==0,ObjVal(s)==0,SolVal(delta)==[0,0],SolVal(x)==[0,0],sum(SolVal(q)) == 1)
  else:
    print(rc)
  s.Add(a[0][0]*x[0]+a[0][1]*x[1] == b[0])
  #s.Add(delta[0] == 1)
  rc = s.Solve()
  if rc == 0:
    #print rc,ObjVal(s),SolVal(delta),SolVal(x)
    print(rc==0,ObjVal(s)==4,SolVal(delta)==[1,0],SolVal(x)==[0,4])
  else:
    print(rc)
  #s.Add(delta[1] == 1)
  s.Add(a[1][0]*x[0]+a[1][1]*x[1] == b[1])
  rc = s.Solve()
  if rc == 0:
    #print rc,ObjVal(s),SolVal(delta),SolVal(x)
    print(rc==0,ObjVal(s)==9,SolVal(delta)==[1,1],SolVal(x)==[5,4])
  else:
    print(rc)
main()
