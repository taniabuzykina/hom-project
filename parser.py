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

    v_lengths = content[3]
    series = content[5]

    end = 7+num_vehicles
    constraints = [content[i] for i in range(7, end)]

    l_lengths = content[end+1]

    departures = content[end+3]
    schedule_types = content[end+5]

    blocked = {i[0]: i[1:] for i in content[end+7:]}

    return num_vehicles, num_lanes, v_lengths, series, constraints, l_lengths, departures, schedule_types
#    # Restructure
#
#    vehicles = {i: {} for i in range(num_vehicles)}
#    lanes = {i: {} for i in range(num_lanes)}
#
#    for v in vehicles.keys():
#        vehicles[v]['length'] = v_lengths[v]
#        vehicles[v]['series'] = v_series[v]
#        vehicles[v]['constraint'] = constraints[v]
#        vehicles[v]['departure'] = departures[v]
#        vehicles[v]['schedule_type'] = schedule_types[v]
#
#    for i in lanes.keys():
#        lanes[i]['length'] = l_lengths[i]
#        lanes[i]['blocked_lanes'] = blocked[i] if i in blocked_lanes.keys() else []
#        #maybe include transposed vehicle constraints
#
#    return vehicles, lanes

def parse(path):
    return parse_content(read_file(path))
