**_ dependencies _**

1. flask

- Web framework that we are using competes with django

2. flask-login

- Provides user session management;
- logging in/out and remembering users sessions
- Stores user's id in the session and lets them log out easily.
- Requires sqlalchemy (super important)

3. flask-sqlalchemy

- Caters for all databases, don't really need sql knowledge

4. flask-cors

- Security

5. psycopg2
   -For our database

**_ Front end _**
Bootstrap

- CSS framework for developing responsive and mobile websites.
- https://getbootstrap.com/docs/5.0/getting-started/introduction/

Reactjs

- JS library used for building user interfaces or UI components

**_ Running database _**
psql -h localhost -p 5432 -U postgres rec

**_ Running the application _**
python main.py
