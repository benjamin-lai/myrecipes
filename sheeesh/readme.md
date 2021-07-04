**_ auth.py _**
Authentication Process

**_ models.py _**
Stores sql queries

**_ views.py _**
Contains Website Routes

**_ starting virtualenv _**
myenv/Scripts/activate

**_ dependencies _**
flask
flask-login
flask-sqlalchemy    # i think this one is not required.
flask-cors
psycopg2

**_ HTML _**
all css references comes from:
https://getbootstrap.com/docs/5.0/getting-started/introduction/
base template contains scripts which all other templates inherits

**_ Running the system _**
python main.py

*** Running database ***
psql -h localhost -p 5432 -U postgres rec

**_ Comments _**
database.ini - file that stores connection parameters.
config.py - reads database.ini file and returns connection parameters. - Establishes connection and disconnects them
