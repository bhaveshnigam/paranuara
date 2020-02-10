# Install instructions

### Steps to install
* Run ```git clone https://github.com/bhaveshnigam/paranuara.git```
> All steps from this point to be run from the root of the project. 
* Run ```source setup.sh```
* Update the paranuara/local_settings.py with relevant settings for MySQL access
* Once settings are updated in local_settings.py, Run ```./manage.py check``` in order to confirm settings are in place.
* Run ```source activate.sh``` to apply the schema structure in database.
* Run ```./manage.py load_data``` to load the provided resource files
* Run ```./manage.py runserver 0.0.0.0:8000``` to run the server in 8000 port, consider changing if the port is already occupied
> On Ubuntu/Debian systems one may be required to run to install mysqlclient build packages
```sudo apt-get install python-dev default-libmysqlclient-dev```

### Resources
Provided resources are kept in ```resources/``` folder accessible from the root of the project

### Endpoints
BASE_URL = ```http://localhost:8000```
> Note: Base URL would be different in case one changes the port intentionally
- Endpoint 1
    - **Endpoint**: Given a company provide all of its employees
    - **URL**: ```<BASE_URL>/civilisation/company/employees/<company_id>/```
    - URL Args:
        - company_id: Refers to index + 1 from companies.json resource file
- Endpoint 2
    - **Endpoint**: List all the mutual friends between 2 individuals
    - **URL**: ```<BASE_URL>/civilisation/citizen/<person_1_id>/common-friends/<person_2_id>/```
    - URL Args:
        - person_1_id: _id as seen in people.json for a relevant person
        - person_2_id: _id as seen in people.json for a relevant person 
- Endpoint 3
    - **Endpoint**: Provide details about individual's favourite food
    - **URL**: ```<BASE_URL>/civilisation/citizen/favourite-food/<person_id>/```
    - URL Args:
        - person_id: _id as seen in people.json for a relevant person


### Test cases
Run ```./manage.py test``` to run test cases