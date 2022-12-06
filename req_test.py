import urequests as requests
import json
import gc
import os

from local.connected_wlan import ConnectedWLAN

wlan = ConnectedWLAN()

post_url = "https://asdasdasdsasdasdhttpbin.org/post"
dweet = { "name" : "a name",
          "place" : "my place",
          "warm" : "no"
          }
i=0
while True:
    i=i+1
    body = json.dumps(dweet)
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(post_url, headers=headers, data=body, timeout=10)
        response_dict = {
            "status_code" : response.status_code,
            "headers" : response.headers,
            "content" : response.content
            }
        response.close()
    except Exception as e:
        print(e)
    print(f"{i} free={gc.mem_free()}")
    print(os.statvfs('/'))

