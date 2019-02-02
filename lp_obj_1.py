import numpy as np
from pulp import *
from parser import parse

file_path = 'instances/instance3.txt'

num_v, num_l, v_lengths, series, equipment, l_lengths, departures, schedule_types, blocked = parse(file_path)

num_p = max(l_lengths) // min(v_lengths) # Number of positions (should be calculated and held as small as possible)
max_departures = max(departures) # latest departure time, we need this for some conditions

print(f"Num Variables: {len(v_lengths)*len(l_lengths)*num_p}")

prob = LpProblem("Scheduling", LpMinimize)

# Indicates whether car v is placed in lane l in position p
X = {(v,l,p): LpVariable(f'x_{v}_{l}_{p}', cat='Binary') for v in range(num_v)
                                                         for l in range(num_l)
                                                         for p in range(num_p)}
# Indicates whether lane l has vehicles of series s
Y = {(l,s): LpVariable(f'y_{l}_{s}', cat='Binary') for l in range(num_l)
                                                   for s in np.unique(series)}
# Indicates how much capacity is left in lane l
C = {l: LpVariable(f'c_{l}', cat='Integer') for l in range(num_l)}

# Indicates whether lane l and l+1 have the same schedule type (Note: 0 means YES, 1 means NO')
Z = {l: LpVariable(f'z_{l}', cat='Binary') for l in range(num_l-1)}

# 1. A vehicle is assigned to exactly one lane.
for v in range(num_v):
    prob += lpSum([X[(v,l,p)] for l in range(num_l)
                              for p in range(num_p)]) == 1

# 2. A lane is occupied by exactly one series - vehicle series in the instance (e.g., only tramways or only trolleybuses).
for l in range(num_l):
    for s in np.unique(series):
        prob += lpSum([X[(v,l,p)] * (series[v] == s) for v in range(num_v)
                                                     for p in range(num_p)]) <= 10000*Y[(l,s)]
    prob += lpSum([Y[(l,s)] for s in np.unique(series)]) <= 1

# 3. A vehicle can be placed only on a lane with the necessary equipment constraints related to lane equipment (e.g., tramways can be parked on lanes with rails, buses on any lane).
for v in range(num_v):
    for l in range(num_l):
            prob += lpSum([X[(v,l,p)] for p in range(num_p)]) <= int(equipment[v][l])

# 4. the sum of vehicle lengths on a lane cannot exceed the lane capacity, while including the distance of 0.5 between vehicles in a lane.
for l in range(num_l):
    prob += lpSum([X[(v,l,p)] * (v_lengths[v] + 0.5)
                             for v in range(num_v)
                             for p in range(num_p)]) - 0.5 + C[l] == l_lengths[l]
    prob += C[l] >= 0
# 5. A vehicle is assigned to exactly one position (number of a vehicle in a lane).
# Implied by 1

# 6. A position is occupied by exactly one vehicle.
for l in range(num_l):
    for p in range(num_p):
        prob += lpSum([X[(v,l,p)] for v in range(num_v)]) <= 1

# 7. The departure time of any vehicle must be prior to the vehicle following it - departure time in the instance.
for l in range(num_l):
    for p in range(num_p-1): #-1 because we don't care about the last
        prob += lpSum([(X[(v,l,p)]-X[(v,l,p+1)]) * departures[v] + X[(v,l,p+1)] * max_departures for v in range(num_v)]) <= max_departures

# 8. The departure of all the vehicles in a blocking lane must be prior to the departure of any vehicle in blocked lanes - blocked lanes.
for p in range(num_p):
    for l in blocked:
        for b in blocked[l]:
            prob += lpSum([(X[(v,l-1,p)]-X[(v,b-1,0)]) * departures[v] + X[(v,b-1,0)] * max_departures for v in range(num_v)]) <= max_departures

# 9. Positions are taken in order, i.e. position x+1 is only taken if x is taken
for l in range(num_l):
    for p in range(num_p-1): #-1 because we don't care about the last
        prob += lpSum([X[(v,l,p+1)]-X[(v,l,p)] for v in range(num_v)]) <= 0

################################################################
#                     OBJECTIVE 1 Specific                     #
################################################################

# Note that Constraint 4. has also been modified for obj 1


for l in range(num_l-1):
    prob += lpSum([X[(v,l,0)]-X[(v,l+1,0)] for v in range(num_v)]) <= Z[l]*1000 #TODO: pick better big M
    prob += lpSum([X[(v,l,0)]-X[(v,l+1,0)] for v in range(num_v)]) >= Z[l]*1000*(-1) #TODO: pick better big M

# Weights
p_1 = 1 / num_l
p_2 = 1 / num_l
p_3 = 1 / (sum(l_lengths) - sum(v_lengths))

# Min function
f_1 = lpSum([Z[l] for l in range(num_l - 1)])
f_2 = lpSum([Y[(l,s)] for l in range(num_l)
                      for s in np.unique(series)])
f_3 = lpSum([C[l] for l in range(num_l)])

prob += p_1 + f_1 + p_2 + f_2 + p_3 + f_3

prob.writeLP("Scheduling.lp")
prob.solve()

print("Status:", LpStatus[prob.status])

#for v in prob.variables():
#    print(v.name, "=", v.varValue)

print("Minimized value =", value(prob.objective))

# Write solution as matrix
solution_matrix = np.zeros((num_v, num_l, num_p))
for v in range(num_v):
    for l in range(num_l):
        for p in range(num_p):
            solution_matrix[v,l,p] = prob.variablesDict()[f'x_{v}_{l}_{p}'].varValue

# Construct solution matrix
result_matrix = np.full((num_l, num_p), None)
for l in range(num_l):
    for p in range(num_p):
        values = solution_matrix[:,l,p]
        if max(values) > 0:
            pos = np.argmax(values)+1
            result_matrix[l,p] = pos

with open(file_path + f'_solution_obj_1_num_p_{num_p}.txt', 'w') as f:
    for l in range(num_l):
        for p in range(num_p):
            f.write(f'{str(result_matrix[l,p]) + " " if result_matrix[l,p] is not None else ""}')
        f.write('\n')
print('Done.')






