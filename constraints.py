#from sympy import Poly, Symbol
#from sympy.solvers.inequalities import reduce_rational_inequalities as reduce
#from sympy.solvers.inequalities import solve_rational_inequalities as solve
#
##result = reduce([[0 <= x + 3]],x)
#
#x, y = Symbol('x'), Symbol('y')
#
#result = solve([[
#    ((Poly(x + y), Poly(x**2)), '>=')]])
#
#print(result)

import numpy as np

dim = 100

A = np.random.normal(size=(dim,dim))
x_init = np.random.normal(size=(dim,))
b = np.random.normal(size=(dim,))

mutate = lambda x, degree, num: [x + np.random.normal(0,degree,x.shape) for _ in range(num)]
def neighbourhood(x, degree, num):
    result = []
    for _ in range(num):
        x_new = x.copy()
        x_new[int(np.random.randint(0,len(x)-1))] += np.random.choice([-1,1])
        result.append(x_new)
    return result

simple_distance = lambda x: np.sum(A @ x < b)

epochs = 10000 
num_phenotypes = 100
degree_mutation = 0.8

cur_phenotypes = [x_init]

for i in range(epochs):
    if i % 2000 == 0: degree_mutation *= 0.8
    cur_best_phenotype = None
    cur_best_distance = 10000 
    for c in cur_phenotypes:
        dist = simple_distance(c)
        if dist < cur_best_distance:
            cur_best_distance = dist
            cur_best_phenotype = c
    print(f'[{str(i).zfill(4)}] best distance: {cur_best_distance}')
    cur_phenotypes = neighbourhood(cur_best_phenotype, degree_mutation, num_phenotypes)
