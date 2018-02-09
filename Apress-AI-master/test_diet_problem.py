
from tableutils import printmat,wrapmat,formatmat
from diet_problem import gen_diet_problem, solve_diet
import random
import sys
def main():
  if len(sys.argv)==1:
    return
  elif len(sys.argv)==3:
    random.seed(int(sys.argv[2]))
  nbfoods=5
  nbnutrients=4
  header=['']+['N'+str(i) for i in range(nbnutrients)]+['Min','Max','Cost','Solution']
  table=gen_diet_problem(nbfoods,nbnutrients)
  rc,value,solution=solve_diet(table)
  T=[0]*nbnutrients
  C=0
  for food in range(nbfoods):
    C=C+solution[food]*table[food][nbnutrients+2]
    for nutrient in range(nbnutrients):
      T[nutrient] = T[nutrient]+solution[food]*table[food][nutrient]
  for i in range(nbnutrients):
    T[i]=int(round(T[i],0))
  T=T+['','',round(C,2),'']
  table=table+[T]
  for i in range(0,nbfoods):
    table[i]=table[i]+[round(solution[i],2)]


  wrapmat(table,['F'+str(i) for i in range(nbfoods)]+['Min','Max','Sol'],header);
  printmat(formatmat(wrapmat(table,['F'+str(i) for i in range(nbfoods)]+['Min','Max','Sol'],header),True,4))
main()
