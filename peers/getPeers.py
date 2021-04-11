import btdht
import binascii
import json
from time import sleep
import ipinfo
import aiofiles
import asyncio
import time
import numpy as np
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter
import sys


async def get_peers_info(torrent):
    name = torrent['name']
    infohash = torrent['infohash']
    number_of_peers = torrent['peers']

    i = 3
    peers = []

    timeout = time.time() + 20

    print('Getting peers...')
    while i > 0:
        if time.time() > timeout:
            print('Timeout has been reached...')
            break
        aux = dht.get_peers(binascii.a2b_hex(infohash))
        if aux != None:
            i = i-1
            peers = peers + aux
        sleep(1)

    peers = list(dict.fromkeys(peers))

    #If we found no peers, we quit this function
    if not peers:
        return

    async with aiofiles.open('data/PeersInformation.csv', mode="a") as afp:
        writer = AsyncWriter(afp, dialect="unix")
        
        print('Getting peer details!')
        peers_info = []
        for peer in peers:
            ip = peer[0]
            details = handler.getDetails(ip).all
            
            json_object = {}

            for field in header:
                if field not in details:
                    json_object[field] = 'null'
                else:
                    json_object[field] = details[field]
            
            json_object['name'] = name

            peers_info.append(list(json_object.values()))
        
        print('Writing on file...')
        await writer.writerows(peers_info)

async def writeHeader(header):
    async with aiofiles.open('data/PeersInformation.csv', mode="a") as afp:
        writer = AsyncWriter(afp, dialect="unix")
        await writer.writerow(header)

access_token = '8c90c85de0a0ca'
handler = ipinfo.getHandler(access_token)

dht = btdht.DHT()
dht.start()
sleep(15) # wait for the DHT to build

if not sys.argv[1]:
    print('Insert a filename')
else:
    #gets first argument with the name of the file
    with open(sys.argv[1]) as json_file:
        data = json.load(json_file)

    #creating csv file and writing the header
    data_filename = open('data/PeersInformation.csv', 'w')

    header = ['ip', 'hostname', 'city', 'region', 'country','name']
    asyncio.run(writeHeader(header))

    #go through all torrents
    for torrent in data:
        asyncio.run(get_peers_info(torrent))