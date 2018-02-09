
from features import gen_features, solve_classification
from margins import solve_margins_classification
import sys
import random
import tableutils

def main():
  n=12
  m=2
  if len(sys.argv)<=1:
    print('Usage is main [gen|run] [seed]')
    return
  elif len(sys.argv)>=2:
    if len(sys.argv)>=3:
      random.seed(int(sys.argv[2]))
    A,B,a=gen_features(n,m)
    C = [[A[i][0],A[i][1],B[i][0],B[i][1]] for i in range(len(A))]
    if sys.argv[1]=='gen':
      C.insert(0,['A-Radius','A-Perimeter','B-Radius','B-Perimeter'])
      tableutils.printmat(C,True)
    elif sys.argv[1]=='plane':
      a=[a]
      a.insert(0,['a1','a2','a0'])
      tableutils.printmat(a)
    elif sys.argv[1]=='run':
      rc,Value,G=solve_classification(A,B)
      T=[[[rc,Value],G]]
      tableutils.printmat(T)
    elif sys.argv[1]=='margins':
      rc,a=solve_margins_classification(A,B)
      if rc==0:
        low = min([A[i][0] for i in range(len(A))]+[B[i][0] for i in range(len(B))])
        high = 1+max([A[i][0] for i in range(len(A))]+[B[i][0] for i in range(len(B))])
        T=[[x,a[2]/a[1]-a[0]/a[1]*x] for x in range(low,high)]
      else:
        T=[['Infeasible']]
      tableutils.printmat(T,True)
main()
