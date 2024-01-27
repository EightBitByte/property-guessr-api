import json
import urllib.parse
import urllib.request
from collections import namedtuple

LICENSE_KEY = "Py2dUqCOzoUdp00kL51hjZ**nSAcwXpxhQ0PC2lXxuDAZ-**"
BASE_LOOKUP_PROPERTY_URL = "https://property.melissadata.net/v4/WEB/LookupProperty"

class MelissaAPI:
    def __init__(self, freeform_address : str):
        self.base_url = BASE_LOOKUP_PROPERTY_URL
        self.full_url = self._build_url(freeform_address)

    def _build_url(self, address) -> str:
        parameters = {
            'id': LICENSE_KEY,
            'format' : 'json',
            'ff': address
        }

        encoded_param = urllib.parse.urlencode(parameters)
        url_w_param = f'{self.base_url}?{encoded_param}'
        return url_w_param
    
    def request_data(self):
        try:
            response = urllib.request.urlopen(self.full_url)
            data = response.read().decode(encoding="utf-8")
            json_data = json.loads(data)
            # print(json_data['Records'][0]['Tax']['AssessedValueTotal'])
            return json_data
        except Exception as e:
            print(f"Error: {e}")
        finally:
            response.close()

def filter_data(json_data):
    """
    Get value in key:   'Tax' -> 'AssessedValueTotal'
                        'PropertyUseInfo' -> 'YearBuilt'
                        'SaleInfo' -> 'DeedLastSalePrice', 'DeedLastSaleDate'
    """
    whole_data = json_data['Records'][0]
    assessed_value_total = whole_data['Tax']['AssessedValueTotal']
    year_built = whole_data['PropertyUseInfo']['YearBuilt']
    last_sale_date = whole_data['SaleInfo']['DeedLastSalePrice']
    last_sale_price = whole_data['SaleInfo']['DeedLastSaleDate']
    filtered_dict = {"assessed_total": assessed_value_total,
                        "build_year": year_built,
                        "last_sale date": last_sale_date,
                        "last_sale_price": last_sale_price
                    }
    return filtered_dict

def main():
    # ff_address = "1030 North Princeton Avenue, Fullerton, CA, 92831"
    ff_address = "1030 North Princeton, Fullerton, CA, 92831"
    lookup_obj = MelissaAPI(ff_address)
    response_data = lookup_obj.request_data()
    filtered_data = filter_data(response_data)
    print(filtered_data)

if __name__ == "__main__":
    main()
        