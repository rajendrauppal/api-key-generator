#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Simple API key generator
1. Generates API keys using random, hashlib and base64 modules.
2. Inserts generated API keys into MongoDB and create an API key pool.
3. Enables clients to ask for an API key, mark the returned API key as used.
4. All subsequent API key requests must not return used API keys from the pool.
"""


__author__ = 'Rajendra Kumar Uppal'
__copyright__ = "Copyright 2015, Rajendra Kumar Uppal"
__credits__ = ["Rajendra Kumar Uppal"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Rajendra Kumar Uppal"
__email__ = "rajen.iitd [at] gmail.com"
__status__ = "Production"


import random
import hashlib
import base64
import pymongo
import argparse


MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "apikeys"
MONGODB_COLLECTION = "keys"
APIKEY_POOL_SIZE = 10


class APIKeyDatabase(object):
    def __init__(self):
        connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
        self.db = connection[MONGODB_DB]
        if MONGODB_COLLECTION in self.db.collection_names():
            self.db.drop_collection(MONGODB_COLLECTION)
        self.collection = self.db[MONGODB_COLLECTION]

    def insert(self, key):
        api_key = {'key':key, 'used':'no'}
        self.collection.insert(api_key)

    def get(self):
        return self.collection.find()


class APIKeyGenerator(object):
    def __init__(self):
        pass

    def generate(self):
        # generate 256-bit number
        num_256bit = str(random.getrandbits(256))

        # cryptographically hash this number using SHA 256
        # the result is base64 encoded
        hashed_num = hashlib.sha256(num_256bit).digest()

        # select random character pair
        char_pair = random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])

        # encode in base64
        b64encoded_str = base64.b64encode(hashed_num, char_pair)

        # get api key
        api_key = b64encoded_str.rstrip('=')
        return api_key


def main():
    arg_parser = argparse.ArgumentParser(description='Enter command line arguments.')
    arg_parser.add_argument('-s', '--pool_size', help='Enter API key pool size, default is 10.')
    args = arg_parser.parse_args()

    pool_size = args.pool_size
    global APIKEY_POOL_SIZE
    if pool_size:
        APIKEY_POOL_SIZE = int(pool_size)

    api_key_gen = APIKeyGenerator()
    api_key_db = APIKeyDatabase()
    for x in range(1, APIKEY_POOL_SIZE + 1):
        key = api_key_gen.generate()
        api_key_db.insert(key)

    keys = api_key_db.get()
    for key in keys:
        print key


if __name__ == '__main__':
    main()
