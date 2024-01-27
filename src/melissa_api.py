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
    
    def request_data_print(self):
        try:
            response = urllib.request.urlopen(self.full_url)
            data = response.read().decode(encoding="utf-8")
            json_data = json.loads(data)
            print(json_data)
            return json_data
        except Exception as e:
            print(f"Error: {e}")

    

def main():
    ff_address = "1030 North Princeton Avenue, Fullerton, CA, 92831"
    lookup_obj = MelissaAPI(ff_address)
    lookup_obj.request_data_print()

if __name__ == "__main__":
    main()
        