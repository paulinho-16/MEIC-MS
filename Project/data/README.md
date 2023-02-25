# Example 

Here we have an example of TAZ and OD_FILE. 
These two files can be used to generate the trips.

## Generate trips 

```bash 
    od2trips -n porto.taz.xml -d od_file.od -o out.trips.xml 
```

## Generate the paths 

Having the trips generated we produce the paths for each car. 

```bash 
    duarouter -c PATH\duarcf_file.trips2routes.duarcfg 
```