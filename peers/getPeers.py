import btdht
import binascii
import json
from time import sleep
import ipinfo
import csv

access_token = '8c90c85de0a0ca'
handler = ipinfo.getHandler(access_token)

dht = btdht.DHT()
dht.start()
sleep(15) # wait for the DHT to build

with open('torrents.json') as json_file:
    data = json.load(json_file)

name = data['name']
infohash = data['infohash']
number_of_peers = data['peers']

i = 3
peers = []

while i > 0:
    print("begin")
    aux = dht.get_peers(binascii.a2b_hex(infohash))
    print("hello")
    if aux != None:
        i = i-1
        peers = peers + aux
    sleep(1)

peers = list(dict.fromkeys(peers))

data_filename = open('data/PeersInformation.csv', 'w')

csv_file = csv.writer(data_filename, delimiter = '|')
header = ['ip', 'hostname', 'city', 'region', 'country']
csv_file.writerow(header)

for peer in peers:
    ip = peer[0]
    details = handler.getDetails(ip).all
    
    json_object = {}

    for field in header:
        if field not in details:
            json_object[field] = 'null'
        else:
            json_object[field] = details[field]

    csv_file.writerow(json_object.values())

