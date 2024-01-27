# database.py
#
# The Python module that connects the AWS RDS database for account storage.
import pymysql
from pathlib import Path

DB_ENDPOINT = "property-guessr-db.c92icgyu6yu1.us-west-1.rds.amazonaws.com"
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
    conn = pymysql.connect(host=DB_ENDPOINT, user=db_username, password=db_password)
    return conn

def execute_query(conn, query):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
    
        conn.commit()

if __name__ == "__main__":
    credentials_path = Path(__file__).parent.parent / "credentials.txt"

    user = ""
    password = ""
    db_name = ""

    with open(credentials_path, 'r') as cred_file:
        user = cred_file.readline().rstrip('\n')
        password = cred_file.readline().rstrip('\n')
        db_name = cred_file.readline().rstrip('\n')

