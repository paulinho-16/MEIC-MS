import sumolib
net = sumolib.net.readNet('./data/porto_clean_laterals.net.xml')

# create TAZ xml file
taz = open('./data/porto.taz.xml', 'w')

taz.write('<tazs>')
outgoing = 0
for node in net.getNodes():
    taz.write('<taz id="%s">' % node.getID())
    for outEdge in node.getOutgoing():
        taz.write('<tazSource id="%s" weight="1"/>' % outEdge.getID())
        outgoing += 1
    for inEdge in node.getIncoming():
        taz.write('<tazSink id="%s" weight="1"/>' % inEdge.getID())
    taz.write('</taz>')
taz.write('</tazs>')
taz.close()
