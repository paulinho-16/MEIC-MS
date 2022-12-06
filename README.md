# feup-ms



# Files description 
## TAZ  
The TAZ (traffic assignment zone) contains the sink and the source edges for the simulation. 

It has the following format:

```xml 
<tazs>
    <taz id="<TAZ_ID>" edges="<EDGE_ID> <EDGE_ID> ..."/>

    ... further traffic assignment zones (districts) ...

</tazs>
``` 

# Commands 

## netconvert
### Generate network
**Converts the osm file to the net**. 

```bash
netconvert --osm porto.osm -o porto_1.net.xml --remove-edges.isolated true --remove-edges.by-vclass private,emergency,authority,army,vip,pedestrian,hov,coach,delivery,moped,bicycle,evehicle,tram,rail_urban,rail,rail_electric,rail_fast,ship
```
### Clean network 
The same command can be used to clean the network by removing decoupled edges and losing nodes.

```bash 
netconvert -s ./data/porto_1.net.xml -o ./data/porto_2.net.xml --remove-edges.isolated true 
```

## Generating the routes
```bash
python tools/randomTrips.py -n data/porto_clean.net.xml -r data/porto.rou.xml -e 50 -l
```

The arguments are: 
- `-r`: generates route file with duarouter;
- `-e`: is the end time;
- `-l`: weight edge probability by length; 

## Generate O/D Matrixes from routes and Taz file

```bash 
python tools/route2OD.py -r <route-file> -a <taz-file> -o <output-file>
```

## Generate brute force Matrix from Taz file 

```bash
python -m genDo.gen_do
```