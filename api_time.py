import requests

def timee():
    servise = ("https://api.majidapi.ir/tools/datetime?token=o53bokgnsnnccwq:OON9LKTPvRXPpvg91rQf")
    req = requests.get(servise)
    j_api = req.json()
    date = j_api["result"]["date"]
    time = j_api["result"]["time"]
    print(date)
    print(time)
    return date , time

timee()