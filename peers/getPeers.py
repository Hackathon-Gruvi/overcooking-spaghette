import btdht
import binascii
from time import sleep
dht = btdht.DHT()
dht.start()
sleep(15) # wait for the DHT to build

while True:
    print(dht.get_peers(binascii.a2b_hex(info_hash)))
    sleep(1)