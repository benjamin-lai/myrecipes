#!/usr/bin/python
# Config file to connect to our database.

import psycopg2
from configparser import ConfigParser

# Reads from database.ini and returns connection paramters
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

# Establishes connection with client and db.
def connect():
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)
        print("Connection to PostgreSQL DB successful")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return conn

# Disconnects user from connection session
def disconnect(conn):
    if conn is not None:
        conn.close()
        print('Database connection closed.')

# Testing
if __name__ == '__main__':
    conn = connect()
    print(conn)
    disconnect(conn)