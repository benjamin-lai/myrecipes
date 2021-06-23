import psycopg2
from login_config import connect, disconnect

account_create_sql = """ INSERT INTO accounts (email, name, password) VALUES (%s,%s,%s)"""

def create_account(email, name, password):
    # connect to the PostgreSQL server
    conn = connect()
    curr = conn.cursor()

    # Execute statement
    account_to_insert = (email, name, password)
    curr.execute(account_create_sql, account_to_insert)
    conn.commit()

    # Close connection
    print(f'Successfully added {email}, {name}, {password} to accounts')
    disconnect(conn)

def get_account():
    # connect to the PostgreSQL server
    conn = connect()
    curr = conn.cursor()

    # Execute statement
    curr.execute('select * from accounts')
    accounts = curr.fetchall()
    print(accounts)
    # Close connection
    disconnect(conn)



# Testing
if __name__ == '__main__':
    get_account()
    create_account('john', 'smith@gmail.com', 'password')
    get_account()