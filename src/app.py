from flask import Flask
from flask import jsonify
import flask
import address
import melissa_api

app = Flask(__name__)

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
        return jsonify({"message": "ERR, WRONG KEY"})
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
