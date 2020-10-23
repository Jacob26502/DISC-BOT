import requests
import json
url="https://api.mcsrvstat.us/2/mc.soton.rocks"

def mcstat():
    r= requests.get(url)
    ##print(r.json())
    return [r.json().get("online"),r.json().get("players"),r.json().get("hostname"),r.json().get("motd").get("clean")[0]]


##returns: online?, players (online and total), server ip, server motd clean
