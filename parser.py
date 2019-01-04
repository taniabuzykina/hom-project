def preprocess(l): #parsing madness because instance encoding is inconsistent (some lines end with space, some don't)
    if len(l) == 0:
        return []
    x = l.split(' ') if l[-1] != ' ' else l[:-1].split(' ')
    return list(map(int, x))

def read_file(path):
    with open(path) as f:
        return list(map(preprocess, f.read().splitlines()))

def parse_content(content):
    num_vehicles = content[0][0]
    num_lanes = content[1][0]

    vehicle_lengths = content[3]
    vehicle_series = content[5]

    end = 7+num_vehicles
    vehicle_constraints = [content[i] for i in range(7, end)]

    lane_lengths = content[end+1]

    vehicle_departures = content[end+3]
    vehicle_schedule_types = content[end+5]

    blocked_lanes = {i[0]: i[1:] for i in content[end+7:]}

    # Restructure

    vehicles = {i: {} for i in range(num_vehicles)}
    lanes = {i: {} for i in range(num_lanes)}

    for v in vehicles.keys():
        vehicles[v]['length'] = vehicle_lengths[v]
        vehicles[v]['series'] = vehicle_series[v]
        vehicles[v]['constraint'] = vehicle_constraints[v]
        vehicles[v]['departure'] = vehicle_departures[v]
        vehicles[v]['schedule_type'] = vehicle_schedule_types[v]

    for i in lanes.keys():
        lanes[i]['length'] = lane_lengths[i]
        lanes[i]['blocked_lanes'] = blocked_lanes[i] if i in blocked_lanes.keys() else []
        #maybe include transposed vehicle constraints

    return vehicles, lanes

def parse(path):
    return parse_content(read_file(path))