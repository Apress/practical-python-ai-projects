
from staffing import gen_data, solve_model
def main():
  import sys
  import random
  import tableutils
  m=12                          # Number of time intervals
  n=7                           # Number of shifts
  n0=4                          # Number of full-time shifts
  header = ['Shift '+str(j) for j in range(n)]
  left = ['{0:02}h'.format(i*2) for i in range(m)]+['Cost']
  if len(sys.argv)<=1:
    print('Usage is main [data|run|runo] [seed]')
    return
  elif len(sys.argv)>=2:
    random.seed(int(sys.argv[2]))
    C=gen_data(m,n,n0)
  if sys.argv[1]=='data':
    tableutils.printmat(tableutils.wrapmat(C,left,header+['Need']),False,2)
  elif sys.argv[1] in ['run', 'runo']:
    if sys.argv[1]=='run':
      rc,Val,x=solve_model(C,n0)
    else:
      rc,Val,x=solve_model(C,n0,None,None,True)
    tableutils.printmat(tableutils.wrapmat([x],['Nb:'+str(sum(x))],['$'+str(Val)]+header),True,0)

main()
