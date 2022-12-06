import sumolib
from xml.dom import minidom

if '__main__' == __name__:
    doc = minidom.Document()
    routes = doc.createElement("routes")
    net = sumolib.net.readNet('./data/porto_clean.net.xml')
    
    route_path = ""
    for edge in net.getShortestPath(net.getEdge("405899851"), net.getEdge("478882416"))[0]:
        route_path += edge.getID() + " "

    for id in range(50):
        vehicle = doc.createElement("vehicle")
        vehicle.setAttribute("id", str(id))
        vehicle.setAttribute("depart", "{:.2f}".format(id))

        route = doc.createElement("route")
        route.setAttribute("edges", route_path)

        vehicle.appendChild(route)
        routes.appendChild(vehicle)

    doc.appendChild(routes)

    with open("./data/porto.rou.xml", "w") as f:
        doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding="UTF-8")
