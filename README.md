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

Converts the osm file to network and performs the following tasks:
- Remove isolated edges (edges without connection); 
- Remove edges that doesn't allow passengers (a default car). 

```bash
netconvert --osm vci.osm -o vci.net.xml --remove-edges.isolated true --remove-edges.by-vclass private,emergency,authority,army,vip,pedestrian,hov,coach,delivery,moped,bicycle,evehicle,tram,rail_urban,rail,rail_electric,rail_fast,ship
```
### Clean network 
The same command can be used to clean the network by removing decoupled edges and losing nodes.

```bash 
netconvert -s ./data/porto_1.net.xml -o ./data/porto_2.net.xml --remove-edges.isolated true 
```

## Duarouter: fix paths 
It might happen that the script creates wrong paths, where exists at least one pair of consecutive edges that doesn't have connection between them. To fix this, we use duarouter command: 

```bash
duarouter --net-file ./data/vci.net.xml --route-files porto_rou.xml --repair -o output
```

## RandomTrips: generating the random routes
```bash
python tools/randomTrips.py -n data/vci.net.xml -r data/vci.rou.xml -e 50 -l
```

The arguments are: 
- `-r`: generates route file with duarouter;
- `-e`: is the end time;
- `-l`: weight edge probability by length; 

## route2OD.py: Generate O/D Matrixes from routes and Taz file

```bash 
python tools/route2OD.py -r <route-file> -a <taz-file> -o <output-file>
```
