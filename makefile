TAZ = ./data/porto.taz.xml 
OD = ./data/porto.od
TRIP = ./data/trips/trips.trips.xml
DUARCFG = ./data/routes/duarcfg_file.trips2routes.duarcfg

# TODO: make clean
gen_od:
	@python ./genOd/gen_od.py

gen_taz: 
	@python ./tools/generateTaz.py

# generates the trips based on the taz and od file. 
gen_trips: 
	@od2trips -n $(TAZ) -d $(OD) -o $(TRIP) --ignore-errors

gen_path:
	@duarouter -c $(DUARCFG) --ignore-errors