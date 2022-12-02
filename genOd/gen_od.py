from xml.dom import minidom 

taz_filepath = "./data/porto.taz.xml"
save_path = "./data/porto.od"

start_file = """$O;D2
* From-Time To-Time
0.00 1.00
* Factor
1.00
*
* some
* additional 
* comments
"""

def read_taz(): 
    f = minidom.parse(taz_filepath)
    return f.getElementsByTagName("taz")

if '__main__' == __name__:
    with open(save_path, 'w') as od_file:
        od_file.write(start_file)
        taz = read_taz()[:10]
        for origin in taz:
            for destiny in taz:
                if origin != destiny:
                    od_file.write(f"\t\t{origin.attributes['id'].value}   {destiny.attributes['id'].value}   1\n")