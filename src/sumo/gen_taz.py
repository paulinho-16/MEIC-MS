import sumolib

def gen_taz():
    net = sumolib.net.readNet('./data/vci.net.xml')

    taz = open('./data/vci.taz.xml', 'w')

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

if __name__ == "__main__":
    gen_taz()