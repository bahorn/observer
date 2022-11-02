import base64
import binascii
import json
import sys
from nacl.public import PublicKey, PrivateKey, Box
from stegano import lsbset
from stegano.lsbset import generators

config = json.load(open('server.json', 'r'))

privkey = PrivateKey(base64.b64decode(config['privkey']))
pubkey = PublicKey(base64.b64decode(config['pubkey']))

sb = Box(privkey, pubkey)
message = binascii.hexlify(
    sb.encrypt(bytes(sys.argv[3], 'ascii'))
).decode('ascii')
print(message)

secret = lsbset.hide(sys.argv[1], message, generators.eratosthenes())
secret.save(sys.argv[2])
