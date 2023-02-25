# MS - VCI Digital Model

## Requirements 
To run this project you need to have installed: 

- [SUMO](https://www.eclipse.org/sumo/)
- [Python](https://www.python.org/)
- [Make](https://www.gnu.org/software/make/)

## Setup 

- Create a python virtual environment:
```
python -m venv env
```

- If you are using linux, then activate the environment: 
```bash
source env/bin/activate # linux
./env/Scripts/activate  # windows 
``` 

- Install the requirements:
```
pip install -r requirements.txt
```

With this you are ready to go! 

## Execution


- Before executing the project run the following command to process the real data:   
```bash 
make data
```

- Now execute the project by typing: 
```bash
make
```

# Configuration  

Any simulation settings should be done in the `config.ini` file, where:

- HOUR_START is the start hour of the period to be analyzed
- HOUR_END is the end hour of the period to be analyzed
- OD_PERCENTAGE is the percentage of the network capacity to be used
- STRATEGY is the calibration approach, described in the report, which can only take the values 1 or 2

