
from __future__ import print_function
from coexistence import solve_coexistence
pop,x=solve_coexistence()
T=[['Specie', 'Count']]
for i in range(3):
  T.append([['Toads','Salamanders','Caecilians'][i], x[i]])
T.append(['Total', pop])
for e in T:
  print (e[0],e[1])
