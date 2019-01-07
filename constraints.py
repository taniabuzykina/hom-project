import numpy as np

num_variables = 100
num_constraints = 20

A = np.random.normal(size=(num_constraints, num_variables))
x_init = np.random.normal(size=(num_variables,))
b = np.random.normal(size=(num_constraints,))

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
degree_mutation = 1

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
