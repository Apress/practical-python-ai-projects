
from maxflow import gen_data, solve_model
def main():
  import sys
  import random
  import tableutils
  n=7
  header=[]
  if len(sys.argv)<=1:
    print('Usage is main [data|run0|run1] [seed]')
    return
  elif len(sys.argv)>=2:
    random.seed(int(sys.argv[2]))
  C,S,T=gen_data(n)
  for i in range(n):
    h='N'+str(i)
    if i in S:
      h=h+'-S'
    elif i in T:
      h=h+'-T'
    header.append(h)
  if sys.argv[1]=='data':
    tableutils.printmat(tableutils.wrapmat(C,header,header))
  elif sys.argv[1][0:3]=='run':
    rc,Fout,Fin,x=solve_model(C,S,T,sys.argv[1][3:4]=='1')
    tableutils.printmat(tableutils.wrapmat(x,header,[str(int(Fout))+'-'+str(int(Fin))]+header))


main()
