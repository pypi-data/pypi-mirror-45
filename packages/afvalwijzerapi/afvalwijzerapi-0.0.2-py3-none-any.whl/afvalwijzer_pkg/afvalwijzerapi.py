from datetime import datetime
import json
import requests

class AfvalwijzerAPI(object):
    def __init__(self, zipCode,number,numberAddition):
        """Initialize the data object."""        

        resource = "http://api.mijnafvalwijzer.nl/webservices/appsinput/?method=postcodecheck&postcode={}&street=&huisnummer={}&toevoeging={}&langs=nl&platform=phone&mobiletype=ios&version=1.3&afvaldata=0&content=0&app_name=RWM&apikey=5ef443e778f41c4f75c69459eea6e6ae0c2d92de729aa0fc61653815fbd6a8ca".format(zipCode,number,numberAddition)        
        self._request = requests.Request('GET', resource, None, None, None).prepare()
        self._data = None
        self.available = False
        self.update()
        
    def getPickupDate(self, garbageType):
        """Gets the pickupdate from the cache"""	
        try:
            for x in self._data["data"]["ophaaldagen"]["data"]:
                pickupDate = datetime.strptime(x["date"], '%Y-%m-%d').date()
                if (pickupDate > datetime.today().date() and (x["type"] == garbageType)):
                    return pickupDate     
            return "unknown"                   
        except:
            return "unknown"

    def update(self):
        """Get the latest data from the AfvalWijzer."""
        try:
            with requests.Session() as sess:
                response = sess.send(self._request, timeout=10, verify=False)
            self._data = json.loads(response.text)
            self.available = True
        except:
            self.available = False
