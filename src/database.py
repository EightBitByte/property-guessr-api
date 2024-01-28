# database.py
#
# The Python module that connects the AWS RDS database for account storage.
import pymysql
from pathlib import Path

DB_ENDPOINT = "guessr-db.c92icgyu6yu1.us-west-1.rds.amazonaws.com"
DB_PORT = 3306 

# ================================================================================ 
# IMPORTANT DEV NOTE: If you don't already have it, create a credentials.txt 
# file outside of this folder with the following syntax:
# <user>
# <password>
# <db name>
# BE SURE NOT TO HAVE ANY SPACES OR TRAILING SPACES!!
# ================================================================================ 

def connect_to_database(db_username: str, db_password: str, db_name: str):
    """
    Connect to the database at DB_ENDPOINT with username and password provided, returning the connection object. 
    """
    conn = pymysql.connect(host=DB_ENDPOINT, user=db_username, password=db_password, database="guessr_db")
    return conn

def execute_query_search(conn, query:str):
    """
    Executes the MySQL query against the targetted connection.
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
        
def execute_query_insert(conn, query:str, values:tuple):
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return 1

def make_search_query(name : str):
    """
    Returns a string for a search query using a certain username
    """
    return f'SELECT * FROM users WHERE username = "{name}";'

def make_insert_query(username: str, profile_image: str,
                        correct_guesses: str, total_guesses: str, 
                        join_data:str):
    """
    Returns a tuple of a string for an insert query and the inputs to be inserted to the database
    """
    base_query = "INSERT INTO users(username, profile_image, correct_guesses, total_guesses, join_date) VALUES(%s, %s, %s, %s, %s);"
    values_tuple = (username, profile_image, correct_guesses, total_guesses, join_data)
    return base_query, values_tuple

# def make_update_query():

if __name__ == "__main__":
    credentials_path = Path(__file__).parent.parent / "credentials.txt"

    user = ""
    password = ""
    db_name = ""

    with open(credentials_path, 'r') as cred_file:
        user = cred_file.readline().rstrip('\n')
        password = cred_file.readline().rstrip('\n')
        db_name = cred_file.readline().rstrip('\n')

    # query = make_search_query("jmoyai")
    query, tuples = make_insert_query('ptum', 'NULL', '20', '21', '2024-01-27 00:00:00')

    connection = connect_to_database(user, password, db_name)
    # result = execute_query_search(connection, query)
    result = execute_query_insert(connection, query, tuples)

    print(result)