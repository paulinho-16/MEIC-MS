from xml.dom import minidom     
import os 

#taz_filepath = "./data/porto_clean.taz.xml"
#save_path = "./data/porto_clean.do.xml"
taz_filepath = "./test/porto.taz.xml"
save_path = "./test/porto.do.xml"

def read_taz(): 
    f = minidom.parse(taz_filepath)
    return (f.getElementsByTagName("tazSource"), f.getElementsByTagName("tazSink"))


def gen_root(): 
    root =  minidom.Document()
    return root 

def gen_node_data(root): 
    node_data = root.createElement("data")
    node_data.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    node_data.setAttribute("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/datamode_file.xsd")
    root.appendChild(node_data)
    return node_data

def gen_node_interval(root, id, begin, end):
    interval = root.createElement("interval")
    interval.setAttribute("id", id)
    interval.setAttribute("begin", begin)
    interval.setAttribute("end", end)
    return interval 

def gen_node_taz_relation(root, count, from_, to):
    taz_relation = root.createElement("tazRelation")
    taz_relation.setAttribute("count", count)
    taz_relation.setAttribute("from", from_)
    taz_relation.setAttribute("to", to)
    return taz_relation


if '__main__' == __name__: 
    (source_nodes, sink_nodes) = read_taz() 
    root = gen_root()        

    data_node = gen_node_data(root)
    root.appendChild(data_node)

    node_interval = gen_node_interval(root, "1", "0", "1:0:0")
    data_node.appendChild(node_interval)

    for source in source_nodes:
        for sink in sink_nodes: 
            relation = gen_node_taz_relation(root, "2", source.attributes["id"].value, sink.attributes["id"].value)
            node_interval.appendChild(relation)

    xml_str = root.toprettyxml(indent ="\t") 
    with open(save_path, "w") as f:
        f.write(xml_str)
