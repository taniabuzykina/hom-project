from pulp import *
from parser import parse

num_v, num_l, v_lengths, series, constraints, l_lengths, departures, schedule_types = parse('instance1.txt')
num_positions = 20
print(f"Num Variables: {len(v_lengths)*len(l_lengths)*num_positions}")

p = Lpplem("Scheduling", LpMinimize)

X = {(v,l,p): LpVariable(f'x_{v}_{l}_{p}', cat='Binary') for v in range(num_v)
                                                         for l in range(num_l)
                                                         for p in range(num_p)} 

Y = {(l,s): LpVariable(f'y_{l}_{s}', cat='Binary') for l in range(num_l)
                                                   for s in range(num_s)}

p += lpSum(...) # Minimize

# 1. A vehicle is assigned to exactly one lane.
for v in range(num_v):
    p += lpSum([X[(v,l,p)] for l in range(num_l)
                           for v in range(num_p)]) == 1

# 2. A lane is occupied by exactly one series - vehicle series in the instance (e.g., only tramways or only trolleybuses).
for l in range(num_l):
    for s in range(num_s):
        p += lpSum([X[(v,l,p)] * (series[v] == s) for v in range(num_v)
                                                  for p in range(num_p)]) <= Y[(l,s)]

    p += lpSum([Y[(l,s)] for s in range(num_s)]) <= 1


# 3. A vehicle can be placed only on a lane with the necessary equipment constraints related to lane equipment (e.g., tramways can be parked on lanes with rails, buses on any lane).


# 4. The sum of vehicle lengths on a lane cannot exceed the lane capacity, while including the distance of 0.5 between vehicles in a lane.


# 5. A vehicle is assigned to exactly one position (number of a vehicle in a lane).


# 6. A position is occupied by exactly one vehicle.


# 7. The departure time of any vehicle must be prior to the vehicle following it - departure time in the instance.


# 8. The departure of all the vehicles in a blocking lane must be prior to the departure of any vehicle in blocked lanes - blocked lanes.




p.writeLP("WhiskasModel.lp")
p.solve()

print("Status:", LpStatus[p.status])

for v in p.variables():
    print(v.name, "=", v.varValue)

print("Total Cost of Ingredients per can = ", value(p.objective))
