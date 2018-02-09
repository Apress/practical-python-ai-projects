def gen_diet_problem(nb_foods=5, nb_nutrients=3):
    from random import randint,uniform
    data = []
    ranges = [10**randint(1,4) for i in range(nb_nutrients)]
    MinMax = [0]*nb_nutrients
    for food in range(nb_foods):
        nutrients = [round(randint(1,ranges[i])) for i in range(nb_nutrients)]
        for i in range(len(nutrients)):
            MinMax[i] += nutrients[i]
        minmax = [randint(0,3),randint(3,10)]
        cost = round(100*uniform(0,10))/100
        v = [food]+nutrients+minmax+[cost]
        data.append(v)
        
    for i in range(len(MinMax)):
        MinMax[i] = MinMax[i]/nb_foods
    data.append([0]+[round(e/4) for e in MinMax]+[0,0,0])
    data.append([0]+[round(e*4) for e in MinMax]+[0,0,0])
    print(data)
    return data
