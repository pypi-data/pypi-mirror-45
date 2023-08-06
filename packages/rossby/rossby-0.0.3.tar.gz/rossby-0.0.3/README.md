## **Rossby**
A wrapper for the National Weather Service API

---

#### Info

Documentation for the National Weather Service API can be found
[here](https://www.weather.gov/documentation/services-web-api#/).

Everything that is used to construct this wrapper is contained in
the directory you are currently in. There are 3 files that wrap the
entire API:

- `rossby.py`
- `api_config.py`
- `default_response.py`

All of the endpoints can be found in the file `api_config.py`,
variable `api_endpoints`. Each key in this dictionary variable
defines the name of a base endpoint that can be called on a
`Rossby()` object. Subsequent key-value pairs represent the unique
methods that can be called on the base endpoint.

----------------------------------

##### Getting Started

```python
from rossby import Rossby


rossby = Rossby()

kunv = rossby.stations.by_id(station_id='KUNV')

print(kunv.geometry)
print(kunv.geometry.coordinates)  # equivalent to kunv.geometry['coordinates']

office = rossby.offices.by_id(office_id='CTP')

print(office.address)
print(office.address.streetAddress)
print(office.responsibleCounties)
```
