TAZ = ./data/porto.taz.xml 
OD = ./data/porto.od
TRIP = ./data/porto.trips.xml
DUARCFG = ./data/duarcfg_file.trips2routes.duarcfg

.PHONY: all 

all: gen_od gen_routes

gen_od:
	@python ./sumo/gen_od.py

gen_routes:
	@python ./sumo/gen_routes.py

clean:
	@echo "Removing files..."
	@rm -f ./data/porto.trips.xml ./data/porto.taz.xml ./data/porto.od ./data/*.rou.xml ./data/*.rou.alt.xml 


# PROCESS_NET =======================================================================================================
# Creates the net from the osm, with only roads for passengers. This is the default vehicle class and denotes regular passenger traffic. 
# Vehicle types: https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html
# netconverter: https://sumo.dlr.de/docs/netconvert.html 
process_net: netconvert clean_net

netconvert:
	netconvert --osm ./data/porto.osm -o ./data/porto_1.net.xml --remove-edges.isolated true --remove-edges.by-vclass private,emergency,authority,army,vip,pedestrian,hov,coach,delivery,moped,bicycle,evehicle,tram,rail_urban,rail,rail_electric,rail_fast,ship

# Remove edges decoupled from the network and losing nodes
clean_net: 
	netconvert -s ./data/porto_1.net.xml -o ./data/porto_2.net.xml --remove-edges.isolated true 

# NET TRIPS ========================================================================================================
process_trip: gen_trips gen_paths 

# generates the trips based on the taz and od file. 
gen_trips: 
	@od2trips -n $(TAZ) -d $(OD) -o $(TRIP) --ignore-errors

# Gets the shortest paths. Executed after gen_trips
gen_path:
	@duarouter -c $(DUARCFG) --ignore-errors

gen_taz: 
	@python ./sumo/gen_taz.py