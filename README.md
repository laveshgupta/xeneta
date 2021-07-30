# xeneta
This repo is created to solve interview assignment- Ratestask

## File Structure
* ratestask_server.py:- This is the starting point of application. Run this file to start the server and the apis. Run this as ```python3 ratestask_server.py```
* ratestask_helper.py:- This file consists of helper functions to server api requests
* logger.py:- This file defined logger for logging messages
* db_connection_pool.py:- This file is used to create DB connection pool and to execute DB queries
* config.py:- This is used to have config for the application
* constants.py:- This file contains all the constants value
* ratestack_config.json:- This json file can be used to alter default values specified in constants.py file
* ratestask_integration_tests.py:- This file consists of some integration tests. Wrote some testcases to show my ability to write test cases. Run this as `python3 ratestask_integration_tests.py`
* ratestask_integration_tests.json:- This file serves as input to integration tests file
* ratestask_unit_tests.py:- This file consists of unit test. Run this as `python3 ratestask_unit_tests.py`
* requirements.txt: This file specifies all the packages to run above application. Run this as `pip3 install -r requirements.txt`

# APIs created
 I have created two APIs even though one was required.

 * API 1: /rates
 This api is used to calculate average price for a day between origin and destination. For example:

```
 http://localhost/rates/?date_from=2016-01-01&date_to=2016-01-1&origin=china_main&destination=northern_europe
 ```

 OUTPUT:-
 ```json
 [
    {
        "day": "2016-01-01", 
        "average_price": 1462
    }
]
 ```
 Here, both origin and destination are parent regions. Both of them have child regions which in turn have ports. This api calculates average for a particular day

 * API 2: /rates_ports
 This api is used to calculate average price for a day between ports belonging to origin and destination. 

 ```
 http://localhost/rates_ports/?date_from=2016-01-01&date_to=2016-01-1&origin=china_main&destination=northern_europe
 ```

 OUTPUT:-
 ```json
 [
    {
        "origin": "CNCWN", 
        "destination": "BEANR", 
        "day": "2016-01-01", 
        "average_price": 1138
    }, 
    {
        "origin": "CNCWN", 
        "destination": "BEZEE", 
        "day": "2016-01-01", 
        "average_price": 1120
    }, 
    {
        "origin": "CNCWN", 
        "destination": "DEBRV", 
        "day": "2016-01-01", 
        "average_price": 1316
    }, 
    {
        "origin": "CNCWN", 
        "destination": "DEHAM", 
        "day": "2016-01-01", 
        "average_price": 828
    }, 
    {
        "origin": "CNCWN", 
        "destination": "DEWVN", 
        "day": "2016-01-01", 
        "average_price": 1100
    }, 
    {
        "origin": "CNCWN", 
        "destination": "DKAAR", 
        "day": "2016-01-01", 
        "average_price": 1178
    }, 
    {
        "origin": "CNCWN", 
        "destination": "RULED", 
        "day": "2016-01-01", 
        "average_price": 1365
    }, 
    {
        "origin": "CNCWN", 
        "destination": "RUULU", 
        "day": "2016-01-01", 
        "average_price": 1313
    }, 
    {
        "origin": "CNCWN", 
        "destination": "SEGOT", 
        "day": "2016-01-01", 
        "average_price": 1464
    }, 
    ...
 ]
 ```

 # Initial Setup

 Install all the dependencies mentioned in requirements.txt. Create a virtualenv and then use pip3 to install dependencies

 ```
 virtualenv <path>
 source <path>/bin/activate
 pip3 instal -r requirements.txt
 ```

 # Run Application

 Activate above created virtualenv, Then run ratestask_server.py file

 ```
 source <path>/bin/activate
 python3 ratestask_server.py
 ```

# Run Integration Tests
Activate above created virtualenv, Then run ratestask_server.py file. While application is running, run ratestask_integration_tests.py

```
source <path>/bin/activate
python3 ratestask_server.py
python3 ratestask_integration_tests.py
```

# Run Unit Tests
Activate above created virtualenv, Then run ratestask_unit_tests.py file.

```
source <path>/bin/activate
python3 ratestask_unit_tests.py
```