# Python Gardena project
Enable control and access to Gardena devices

## How to use
```
REQUIREMENTS = ['pygardena==0.0.10']

from pygardena import PyGardena

gardena  = PyGardena(username, password)

sensors = gardena.get_all_sensors()

for sensor in sensors:
    for ability in sensor.get('abilities'):
   
```
