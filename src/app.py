from flask import Flask
import address
import melissa_api

# Create a Flask application
app = Flask(__name__)

# Define a route and its corresponding view function
@app.route('/api/get_property_info')
def create_json_property_info():
    def generate_address():
        random_address = address.RandomAddress()
        ff_address = random_address.format_address()
        lat_long = random_address.generate_coord()
        return {"address": ff_address, 
                "latitude": lat_long.lat,
                "longitude": lat_long.long}
    
    def generate_property_info(ff_address: str):
        lookup_obj = melissa_api.MelissaAPI(ff_address)
        response_data = lookup_obj.request_data()
        filtered_data = melissa_api.filter_data(response_data)
        return filtered_data
    
    def merge(dict1: dict, dict2: dict):
        return (dict2.update(dict1))

    full_address_dict = generate_address()
    property_info_dict = generate_property_info(full_address_dict['address'])
    merged_dicts = merge(full_address_dict, property_info_dict)
    return merged_dicts

    

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
