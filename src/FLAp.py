from flask import Flask
import addresses

# Create a Flask application
app = Flask(__name__)

# Define a route and its corresponding view function
@app.route('/')
def index():
    ans = f"Address: {addresses.lat_lon_freeform()[2]} Latitude: {addresses.lat_lon_freeform()[0]} Longitude: {addresses.lat_lon_freeform()[1]}"
    return ans

@app.route('/latlon')
def latlon():
    ans = f"Latitude: {addresses.lat_lon_freeform()[0]} Longitude: {addresses.lat_lon_freeform()[1]}"
    return ans

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
