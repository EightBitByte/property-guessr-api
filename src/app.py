from flask import Flask
from flask import jsonify
import flask
import address
import melissa_api
import database
from pathlib import Path

KEY = "923E2A273E796"

app = Flask(__name__)

@app.route('/api/get_user_info')
def get_user_info():
    # TODO: Will contain a query parameter with username and key, do the usual key checking, return row with username
    pass

@app.route('/api/get_leaderboard_info')
def get_leaderboard_info():
    """
    Returns a JSON object which has a list of dictionaries of all the users, else return an error message
    """
    def operate_on_database(json_data):
        """
        Operate on database by getting the executing the "get top 20" users based on streak
        """
        credentials_path = Path(__file__).parent.parent/ "credentials.txt"
        user = ""
        password = ""
        db_name = ""

        with open(credentials_path, 'r') as cred_file:
            user = cred_file.readline().rstrip('\n')
            password = cred_file.readline().rstrip('\n')
            db_name = cred_file.readline().rstrip('\n')

        query = database.get_top_20_query()
        connection = connect_to_database(user, password, db_name)
        return database.execute_query_top_20(connection, query)

    if (flask.request.args.get("key") != KEY):
        return jsonify({"message": "ERR, WRONG KEY"})
    else:
        data = flask.request.json
        top_20 = operate_on_database(data)
        list_of_dict = list()
        for elem in top_20:
            username = i[0]
            profile_image = i[1]
            correct_guesses = i[2]
            total_guesses = i[3]
            join_date = i[4]
            streak = i[5]
            list_of_dict.append({"username": username, "profile_image": profile_image,
                                "correct_guesses": correct_guesses, "total_guesses": total_guesses,
                                "join_date": join_date, "streak": streak})
        return {"list": list_of_dict}

        

@app.route('/api/send_user_info', methods=['POST'])
def receive_user_info():
    """
    Returns a json object if the database update was successful, else return a message
    """
    def update_database(json_data):
        """
        Updates the database based on json data that is received from front-end request
        """
        credentials_path = Path(__file__).parent.parent/ "credentials.txt"
        user = ""
        password = ""
        db_name = ""

        with open(credentials_path, 'r') as cred_file:
            user = cred_file.readline().rstrip('\n')
            password = cred_file.readline().rstrip('\n')
            db_name = cred_file.readline().rstrip('\n')

        #TODO: Check if the user is in the database already before updating, otherwise be sure to create the user
        
        username = json_data["username"]
        corr_guess = json_data["correct_guesses"]
        total_guess = json_data["total_guesses"]
        streak_num = json_data["streak"]
        
        update_query, update_tuples = database.make_update_query(username, corr_guess, total_guess, streak_num)
        connection = database.connect_to_database(user, password, db_name)
        database.execute_query_insert_update(connection, update_query, update_tuples)
    
    if (flask.request.args.get("key") != KEY):
        return jsonify({"message": "ERR, WRONG KEY"})
    else:
        data = flask.request.json
        update_database(data)
        return {"message": "Data received"}


@app.route('/api/get_property_info')
def create_json_property_info():
    """
    Returns a JSON object of a dictionary containing the full address and property information
    """
    def generate_address() -> dict:
        """
        Returns a dictionary of a random address {address, latitude, longitude}
        """
        random_address = address.RandomAddress()
        ff_address = random_address.format_address()
        lat_long = random_address.generate_coord()
        return {"address": ff_address, 
                "latitude": lat_long.lat,
                "longitude": lat_long.long}
    
    def generate_property_info(ff_address: str):
        """
        Returns a dictionary of the property information
        """
        lookup_obj = melissa_api.MelissaAPI(ff_address)
        response_data = lookup_obj.request_data()
        filtered_data = melissa_api.filter_data(response_data)
        return filtered_data

    if flask.request.args.get("key") != "923E2A273E796":
        return jsonify({"message": "Wrong key"})
    else:
        while True:
            try:
                full_address_dict = generate_address()
                property_info_dict = generate_property_info(full_address_dict['address'])
                merged_dicts = full_address_dict | property_info_dict
                return jsonify(merged_dicts)
            except Exception:
                pass

    
if __name__ == '__main__':
    app.run(debug=True)
