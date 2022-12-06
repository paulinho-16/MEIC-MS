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