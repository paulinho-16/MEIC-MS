import re


edges = set([])
sensor_edges = set([])
in_edges = set([])
out_edges = set([])


def get_edges():
    with open ("./routes_map.txt") as f:
        for line in f:
            [in_out, edge_ids] = line.strip().split("::")
            [in_id, out_id] = in_out.split()
            in_edges.add(in_id)
            out_edges.add(out_id)
            for node in edge_ids.split():
                edges.add(node)

def get_detectors():
    with open ("./detectors.add.xml") as f:
        for line in f:
            splitted = line.strip().split("\"")
            if len(splitted) >= 2:
                sensor_id = splitted[1]
                sensor_edge = splitted[3]
                sensor_edges.add((sensor_id, sensor_edge))

get_edges()
get_detectors()

print(sensor_edges)