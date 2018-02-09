
from __future__ import print_function
from tsp import gen_data, solve_model, solve_model_eliminate, solve_model_p, solve_model_star
def main():
  import sys
  import random
  import tableutils
  n=10
  if len(sys.argv)<=1:
    print('Usage is main [data|display|run|path|star] [seed]')
    return
  elif len(sys.argv)>2:
    random.seed(int(sys.argv[2]))
  C,Points=gen_data(n)
  header = ['P (x y)']+['P'+str(i) for i in range(n)]
  left = ['P'+str(i)+' '+str(Points[i][0])+' '+str(Points[i][1])+' ' for i in range(n)]
  if sys.argv[1]=='data':
    tableutils.printmat(tableutils.wrapmat(C,left,header),False,1)
  elif sys.argv[1]=='display':
    subtours=[]  
    tours = []
    count = 0
    display = []
    while count < 10 and len(tours) != 1:
      rc,Value,tours=solve_model_eliminate(C,subtours)
      subtours.extend(tours)
      display.append(['{0}-({1})'.format(count,int(Value))]+[tour for tour in tours])
      count += 1
    display.insert(0,['Iter (value)','Tour(s)'])
    for row in display:
      l=''
      for i in range(1,len(row)):
        l=l+' '+str(row[i])
        if i < len(row)-1:
          l=l+';'
      print('{0}, "{1}"'.format(row[0],l))
  elif sys.argv[1]=='run':
      rc,Value,tours=solve_model(C)    
      T=[tours]
      Cost=[0]
      for i in range(n):
        Cost.append(C[tours[i]][tours[(i+1)%len(tours)]])
      T.append(Cost)
      tableutils.printmat(T,True)
  elif sys.argv[1]=='path':
      rc,Value,path=solve_model_p(C)    
      T=[['Nodes']+path]
      Cost=['Distance',0]
      Tcost=['Cumulative',0]
      for i in range(n-1):
        Cost.append(C[path[i]][path[(i+1)]])
        Tcost.append(Tcost[-1]+Cost[-1])
      #Cost.append('Total:'+str(Value))
      T.append(Cost)
      T.append(Tcost)
      tableutils.printmat(T,True)
  elif sys.argv[1]=='star':
      rc,Value,Tour=solve_model_star(C)    
      Tour.append(Tour[0])
      T=[Tour]
      Cost=['Total dist '+str(int(Value)),0]
      for i in range(len(Tour)-1):
        Cost.append(C[Tour[i]][Tour[(i+1)%len(Tour)]])
      Tour.insert(0,'NB '+str(len(Tour)))
      T.append(Cost)
      tableutils.printmat(T,True)
main()
