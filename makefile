TAZ = ./example/porto.taz.xml 
OD = ./example/od_file.od 
TRIP = ./example/out.trips.xml
DUARCFG = ./example/duarcfg_file.trips2routes.duarcfg

# generates the trips based on the taz and od file. 
gen_trips: 
	@od2trips -n $(TAZ) -d $(OD) -o $(TRIP)

gen_path:
	@duarouter -c $(DUARCFG)