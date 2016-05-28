
# py-iata-lookup

Small API powered by a simple python flask example which exposes a search form on [iata.org](http://www.iata.org/publications/Pages/code-search.aspx) where you're able to search for airlines and airports based on name or code.

## Setup and usage

You need to have [python 2.7 and pip](http://docs.python-guide.org/en/latest/starting/install/win/) and install the following python modules:

	pip install -r pip_requirements.txt

Open a terminal in this repository and run

	python app.py

You're now running a local instance of the py-iata-lookup API on your localhost:15000.

## Examples

Note: the `pretty` parameter is optional, it just prettifies the json response.

[localhost:15000/](http://localhost:15000/)

	https://github.com/Loknar/py-iata-lookup

[localhost:15000/airline/code/ww?pretty=true](http://localhost:15000/airline/code/ww?pretty=true)

	{
		"results": [
			{
				"accounting_code": "377", 
				"airline_name": "WOW Air ehf", 
				"airline_prefix_code": "377", 
				"iata_code": "WW"
			}
		]
	}

[localhost:15000/airline/name/Norwegian?pretty=true](http://localhost:15000/airline/name/Norwegian?pretty=true)

	{
		"results": [
			{
				"accounting_code": "329", 
				"airline_name": "Norwegian Air International LTD.", 
				"airline_prefix_code": "329", 
				"iata_code": "D8*"
			}, 
			{
				"accounting_code": null, 
				"airline_name": "Norwegian Air Norway AS", 
				"airline_prefix_code": null, 
				"iata_code": "DH*"
			}, 
			{
				"accounting_code": "328", 
				"airline_name": "Norwegian Air Shuttle A.S.", 
				"airline_prefix_code": "328", 
				"iata_code": "DY*"
			}, 
			{
				"accounting_code": "762", 
				"airline_name": "Norwegian Air UK ltd", 
				"airline_prefix_code": "762", 
				"iata_code": "DI"
			}
		]
	}

[localhost:15000/location/name/London?pretty=true](http://localhost:15000/location/name/London?pretty=true)

	{
		"results": [
			{
				"airport_code": "ELS", 
				"airport_name": "East London", 
				"city_code": "ELS", 
				"city_name": "East London"
			}, 
			{
				"airport_code": "GON", 
				"airport_name": "Airport", 
				"city_code": "GON", 
				"city_name": "Groton/New London"
			}, 
			{
				"airport_code": "BQH", 
				"airport_name": "Biggin Hill", 
				"city_code": "LON", 
				"city_name": "London"
			}, 
			{
				"airport_code": "LCY", 
				"airport_name": "City Airport", 
				"city_code": "LON", 
				"city_name": "London"
			}, 
			{
				"airport_code": "LGW", 
				"airport_name": "Gatwick", 
				"city_code": "LON", 
				"city_name": "London"
			}, 
			{
				"airport_code": "LHR", 
				"airport_name": "Heathrow", 
				"city_code": "LON", 
				"city_name": "London"
			}, 
			{
				"airport_code": "LON", 
				"airport_name": "Metropolitan Area", 
				"city_code": "LON", 
				"city_name": "London"
			}, 
			{
				"airport_code": "LTN", 
				"airport_name": "Luton", 
				"city_code": "LON", 
				"city_name": "London"
			}, 
			{
				"airport_code": "SEN", 
				"airport_name": "Southend", 
				"city_code": "LON", 
				"city_name": "London"
			}, 
			{
				"airport_code": "STN", 
				"airport_name": "Stansted", 
				"city_code": "LON", 
				"city_name": "London"
			}, 
			{
				"airport_code": "YXU", 
				"airport_name": "International", 
				"city_code": "YXU", 
				"city_name": "London"
			}, 
			{
				"airport_code": "LOZ", 
				"airport_name": "Magee Field", 
				"city_code": "LOZ", 
				"city_name": "London/Corbin"
			}, 
			{
				"airport_code": "LYX", 
				"airport_name": "London Ashford", 
				"city_code": "LYX", 
				"city_name": "Lydd"
			}, 
			{
				"airport_code": "OXF", 
				"airport_name": "London Oxford", 
				"city_code": "OXF", 
				"city_name": "Oxford"
			}
		]
	}

[localhost:15000/location/code/YYZ?pretty=true](http://localhost:15000/location/code/YYZ?pretty=true)

	{
		"results": [
			{
				"airport_code": "YYZ", 
				"airport_name": "Lester B. Pearson Intl", 
				"city_code": "YTO", 
				"city_name": "Toronto"
			}
		]
	}

## Licence

WTFPL
