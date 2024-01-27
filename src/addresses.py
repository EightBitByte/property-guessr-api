from random_address import real_random_address_by_state
import random
from collections import namedtuple

Coord = namedtuple("Coord", ['lat', 'long'])

class RandomAddress:
    """
    A class that serves to generate a random address
    """
    def __init__(self):
        self._state = "CA"
        self._address = self._generate_random_address()
    
    def _generate_random_address(self) -> dict:
        """
        Returns a random address in the form of a dictionary using the random_address library
        """
        address_dict = real_random_address_by_state("CA")
        return address_dict

    def format_address(self) -> str:
        """
        Returns a formated string of the random address
        """
        address_dict = self._address
        return f"{address_dict['address1']}, {address_dict['city']}, {address_dict['state']}, {address_dict['postalCode']}"

    def generate_coord(self) -> Coord(float, float):
        """
        Returns a namedtuple of the coordinates (latitude, longitude) of the random address
        """
        address_dict = self._address
        coordinates = Coord(address_dict['coordinates']['lat'], address_dict['coordinates']['lng'])
        return coordinates

def lat_lon_freeform() -> (float, float, str):
    addy = random_address.real_random_address_by_state("CA")
    address1 = addy['address1'] + ","
    city = addy['city'] + ", CA,"
    postal = addy['postalCode']
    freeform = "{in1} {in2} {in3}".format(in1=address1, in2=city, in3=postal)
    #print('String Concatenation using format() =', freeform)
    #print(addy['coordinates']['lat'], addy['coordinates']['lng'], freeform)
    return (addy['coordinates']['lat'], addy['coordinates']['lng'], freeform)    

def main():
    some_address = RandomAddress()
    print(some_address.format_address())
    print(some_address.generate_coord())
    


if __name__ == "__main__":
    main()