import requests
import json
url="https://api.mcsrvstat.us/2/151.80.213.47:25635"

def mcstat():
    r= requests.get(url)
    ##print(r.json())
    if r.json().get("online")==True:
        onlineState="Yes"
    else:
        onlineState="No"
    return [onlineState,r.json().get("players"),str(r.json().get("ip"))+":"+str(r.json().get("port")),r.json().get("motd").get("clean")[0]]


##returns: online?, players (online and total), server ip, server motd clean
