import sys
import base64
import json
import nacl.utils
from nacl.public import PrivateKey

privkey = PrivateKey.generate()
pubkey = privkey.public_key


def gen_keypair():
    return (
        base64.b64encode(bytes(privkey)).decode('ascii'),
        base64.b64encode(bytes(pubkey)).decode('ascii')
    )

client = gen_keypair()
server = gen_keypair()

client_config = {
    'privkey': client[0],
    'pubkey': server[1],
    'path': sys.argv[1]
}

server_config = {
    'privkey': server[0],
    'pubkey': client[1]
}

cc = open('client.json', 'w')
sc = open('server.json', 'w')

json.dump(client_config, cc)
json.dump(server_config, sc)

cc.close()
sc.close()
