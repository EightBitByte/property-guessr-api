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

def execute_query_search(conn, query:str, isFetchOne:bool):
    """
    Executes the MySQL search query against the targetted connection.
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        if isFetchOne:
            results = cursor.fetchone()
        else:
            results = cursor.fetchall()
        cursor.close()
        return results
        
def execute_query_insert_update(conn, query:str, values:tuple) -> int:
    """
    Executes the MySQL insert query against the targetted connection
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return 1
    
def execute_query_top_20(conn, query:str):
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return list(results)

def make_search_query(name : str):
    """
    Returns a string for a search query using a certain username
    """
    if name == "":
        return f'SELECT * FROM users;'
    else:
        return f'SELECT * FROM users WHERE username = "{name}";'

def make_insert_query(username: str, profile_image: str,
                        correct_guesses: str, total_guesses: str, 
                        join_data:str) -> str:
    """
    Returns a tuple of a string for an insert query and the inputs to be inserted to the database
    """
    base_query = "INSERT INTO users(username, profile_image, correct_guesses, total_guesses, join_date, streak) VALUES(%s, %s, %s, %s, %s, %s);"
    values_tuple = (username, profile_image, correct_guesses, total_guesses, join_data, '0')
    return base_query, values_tuple

def make_update_query(username: str, correct_guesses: str, total_guesses: str, streak:str):
    """
    Returns a string for an update query
    """
    base_query = "UPDATE users SET correct_guesses = %s, total_guesses = %s, streak = %s WHERE username = %s;"
    values_tuple = (correct_guesses, total_guesses, streak, username)
    return base_query, values_tuple

def get_top_20_query() -> str:
    return f'SELECT * FROM users ORDER BY streak DESC LIMIT 20'

if __name__ == "__main__":
    credentials_path = Path(__file__).parent.parent / "credentials.txt"

    user = ""
    password = ""
    db_name = ""

    with open(credentials_path, 'r') as cred_file:
        user = cred_file.readline().rstrip('\n')
        password = cred_file.readline().rstrip('\n')
        db_name = cred_file.readline().rstrip('\n')

    query = make_search_query("")
    # query, tuples = make_insert_query('lmao', 'NULL', '20', '21', 'CURRENT_TIMESTAMP')
    # query, tuples = make_update_query('jmoyai', 12, 34, 5)
    # query = get_top_20_query()

    connection = connect_to_database(user, password, db_name)

    result = execute_query_search(connection, query, False)
    # result = execute_query_insert_update(connection, query, tuples)
    # result = execute_query_top_20(connection, query)

    print(result)