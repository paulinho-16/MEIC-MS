import sumolib
net = sumolib.net.readNet('porto_clean.net.xml')

# create TAZ xml file
taz = open('porto.taz.xml', 'w')

taz.write('<tazs>')
for node in net.getNodes():
    taz.write('<taz id="%s">' % node.getID())
    for outEdge in node.getOutgoing():
        taz.write('<tazSource id="%s"/>' % outEdge.getID())
    for inEdge in node.getIncoming():
        taz.write('<tazSink id="%s"/>' % inEdge.getID())
    taz.write('</taz>')
taz.write('</tazs>')
taz.close()
