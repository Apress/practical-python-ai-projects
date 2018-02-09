
from __future__ import print_function
from multi_commodity_flow import gen_data,solve_model,solve_all_pairs
import shortest_path
def main():
  import sys
  import random
  import tableutils
  n=5
  m=3
  C=[]
  if len(sys.argv)<=1:
    print('Usage is main [data|run|pairs] [seed]')
    return
  elif len(sys.argv)>2:
    random.seed(int(sys.argv[2]))
  C,Cap=gen_data(n,m)
  if sys.argv[1]=='data':
    for j in range(m):
      for i in range(n):
        C[j][i].insert(0,'N'+str(i))
      C[j][-1].insert(0,'Demand')
      C[j].insert(0,['Comm '+str(j)]+['N'+str(i) for i in range(n)]+['Supply'])
      tableutils.printmat(C[j])
  elif sys.argv[1]=='run':
    rc,Val,x=solve_model(C,Cap,True)
    for j in range(m):
      for i in range(n):
        x[j][i].insert(0,'N'+str(i))
      x[j].insert(0,['Comm '+str(j)]+['N'+str(i) for i in range(n)])
      tableutils.printmat(x[j])
  elif sys.argv[1]=='pairs':
    n=13
    S=[0,2]
    if len(sys.argv)>2:
      random.seed(int(sys.argv[2]))
    C = shortest_path.gen_data(n)    
    rc,Paths,Costs=solve_all_pairs(C,S)
    for i in range(len(S)):
      print('{0}-Target'.format(S[i]),'Cost','[Path]')
      for v in range(n):
        if v != S[i]:
          print(v,Costs[i][v],'{0}'.format(Paths[i][v]))
main()
