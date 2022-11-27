import urequests as requests
import json
from local.logger import Logger

__log = Logger("Dweeter")
class Dweeter:
    def __init__(self, thing):
        __log.debug(f"__init__({thing})")
        self.thing = thing
    
    def dweet(self, dweet):
        __log.debug(f"dweet: {self.thing}")
        
        success = False
        try:
            success = self.__try_dweet(dweet)
        except OSError as err:
            if err.errno == -6:
                __log.error(err, "Perhaps the WLAN isn't connected?")
            raise err
        
        __log.debug(f"dweet: {success}")
        return success

    def __try_dweet(self, dweet):
        post_url = f"https://dweet.io:443/dweet/quietly/for/{self.thing}"
        __log.debug(f"post_url={post_url}")
        
        body = json.dumps(dweet)
        __log.debug(f"body={body}")
        
        headers = {'Content-Type': 'application/json'}
        __log.debug(f"headers={headers}")
        
        response = requests.post(post_url, headers=headers, data=body)
        response_dict = {
            "status_code" : response.status_code,
            "headers" : response.headers,
            "content" : response.content
        }
        response.close()
        __log.debug("response:", response_dict)
        
        return response.status_code == 204
