import sumolib
from xml.dom import minidom 

taz_filepath = "./data/porto.taz.xml"
save_path = "./data/porto.od"
complete_net_file = "./data/porto_clean.net.xml"   # Netfile with more than the VCI
start_file = """$O;D2
* From-Time To-Time
0.00 1.00
* Factor
1.00
*
* some
* additional
* comments
* start
"""

def read_taz(): 
    f = minidom.parse(taz_filepath)
    return f.getElementsByTagName("taz")

def create_od_from_taz():
    with open(save_path, 'w') as od_file:
        od_file.write(start_file)
        taz = read_taz()[:10]
        for origin in taz:
            for destiny in taz:
                if origin != destiny:
                    od_file.write(f"\t\t{origin.attributes['id'].value}   {destiny.attributes['id'].value}   1\n")

def generate_od(nodes):
    entry_nodes = []
    exit_nodes = []

    for node in nodes:
        if not node.getIncoming() and node.getOutgoing():
            entry_nodes.append(node.getID())
        elif not node.getOutgoing() and node.getIncoming():
            exit_nodes.append(node.getID())

    with open(save_path, 'w') as od_file:
        od_file.write(start_file)
        for origin in entry_nodes:
            for destination in exit_nodes:
                if origin != destination:
                    #print(f"{origin} {destination}")
                    od_file.write(f"\t\t{origin}   {destination}   1\n")

if '__main__' == __name__:
    net = sumolib.net.readNet(complete_net_file)
    nodes = net.getNodes()
    generate_od(nodes)