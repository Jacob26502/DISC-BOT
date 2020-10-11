import requests
import json
url="https://api.waa.ai/v2/links"
myToken = '<bEE8b752dcbad37b07509a6eFc0a18F63e8e9faa>'
head = {'Authorization': "API-Key bEE8b752dcbad37b07509a6eFc0a18F63e8e9faa"}

body = {"JSON"}

def urlshort(urlin):
    data = {'url': str(urlin)}
    r= requests.post(url, headers=head, json=data)

    link=(str(r.json())[str(r.json()).find("short_code")+14:str(r.json()).find("short_code")+18])
    return link
