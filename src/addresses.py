#from random_address import real_random_address
import random_address
#random_address.real_random_address_by_state('CA')
#we must get random state!!

import random

#f”{address1}, {city}, {state}, {postalCode}
#Ex. “1030 North Princeton Avenue, Fullerton, CA, 92831”


def lat_lon_freeform() -> (float, float, str):
    addy = random_address.real_random_address_by_state("CA")
    address1 = addy['address1'] + ","
    city = addy['city'] + ", CA,"
    postal = addy['postalCode']
    freeform = "{in1} {in2} {in3}".format(in1=address1, in2=city, in3=postal)
    #print('String Concatenation using format() =', freeform)
    #print(addy['coordinates']['lat'], addy['coordinates']['lng'], freeform)
    return (addy['coordinates']['lat'], addy['coordinates']['lng'], freeform)    
#lat/lon ??
def main():
    lat_lon_freeform()


if __name__ == "__main__":
    main()