TAZ = ./data/porto.taz.xml 
OD = ./data/porto.od
TRIP = ./data/porto.trips.xml
DUARCFG = ./data/duarcfg_file.trips2routes.duarcfg

.PHONY: all 

all: gen_taz gen_od gen_trips gen_path

gen_taz: 
	@python ./tools/generateTaz.py

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