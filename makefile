TAZ = ./data/porto.taz.xml 
OD = ./data/porto.od
TRIP = ./data/porto.trips.xml
DUARCFG = ./data/duarcfg_file.trips2routes.duarcfg

.PHONY: all 

all: gen_taz gen_od gen_trips gen_path

gen_taz: 
	@python ./genOd/gen_taz.py

# TODO: make clean
gen_od:
	@python ./genOd/gen_od.py

# generates the trips based on the taz and od file. 
gen_trips: 
	@od2trips -n $(TAZ) -d $(OD) -o $(TRIP) --ignore-errors

gen_path:
	@duarouter -c $(DUARCFG) --ignore-errors

clean:
	@echo "Removing files..."
	@rm -f ./data/porto.trips.xml ./data/porto.taz.xml ./data/porto.od ./data/*.rou.xml ./data/*.rou.alt.xml


# OTHERS =======================================================================================================
# Creates the net from the osm, with only roads for passengers. This is the default vehicle class and denotes regular passenger traffic. 
# Vehicle types: https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
# netconverter: https://sumo.dlr.de/docs/netconvert.html 
netconvert:
	netconvert --osm ./data/porto.osm -o ./data/porto_1.net.xml --remove-edges.isolated true --remove-edges.by-vclass private,emergency,authority,army,vip,pedestrian,hov,coach,delivery,moped,bicycle,evehicle,tram,rail_urban,rail,rail_electric,rail_fast,ship

# Remove edges decoupled from the network 
clean_net: 
	netconvert -s ./data/porto_1.net.xml -o ./data/porto_2.net.xml --remove-edges.isolated true 
