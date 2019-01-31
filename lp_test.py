import numpy as np
from pulp import *
from parser import parse

num_v, num_l, v_lengths, series, equipment, l_lengths, departures, schedule_types, blocked = parse('instance1.txt')

num_p = 20 # Number of positions (should be calculated and held as small as possible)

print(f"Num Variables: {len(v_lengths)*len(l_lengths)*num_p}")

prob = LpProblem("Scheduling", LpMinimize)

X = {(v,l,p): LpVariable(f'x_{v}_{l}_{p}', cat='Binary') for v in range(num_v)
                                                         for l in range(num_l)
                                                         for p in range(num_p)} 

Y = {(l,s): LpVariable(f'y_{l}_{s}', cat='Binary') for l in range(num_l)
                                                   for s in np.unique(series)}

# Min function
prob += 10#lpSum([Y[(l,s)] for l in range(num_l)
        #             for s in np.unique(series)])

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
        for p in range(num_p):
            prob += X[(v,l,p)] <= int(equipment[v][l])

# 4. the sum of vehicle lengths on a lane cannot exceed the lane capacity, while including the distance of 0.5 between vehicles in a lane.
for l in range(num_l):
    prob += lpSum([X[(v,l,p)] * (v_lengths[v] + 0.5) 
                             for v in range(num_v)
                             for p in range(num_p)]) - 0.5<= l_lengths[l]

# 5. A vehicle is assigned to exactly one position (number of a vehicle in a lane).
# Implied by 1

# 6. A position is occupied by exactly one vehicle.
for l in range(num_l):
    for p in range(num_p):
        prob += lpSum([X[(v,l,p)] for v in range(num_v)]) <= 1

# 7. The departure time of any vehicle must be prior to the vehicle following it - departure time in the instance.
for l in range(num_l):
    for p in range(num_p-1): #-1 because we don't care about the last
        prob += lpSum([X[(v,l,p)]-X[(v,l,p+1)]*departures[v] for v in range(num_v)]) <= 0

# 8. The departure of all the vehicles in a blocking lane must be prior to the departure of any vehicle in blocked lanes - blocked lanes.
for v in range(num_v):
    for l in blocked:
        for b in blocked[l]:
            prob += lpSum([X[(v,l,p)]-X[(v,b,p)] for p in range(num_p)]) * departures[v] <= 0

prob.writeLP("Scheduling.lp")
prob.solve()

print("Status:", LpStatus[prob.status])

#for v in prob.variables():
#    print(v.name, "=", v.varValue)

print("Minimized value = ", value(prob.objective))
