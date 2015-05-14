#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Simple API key generator
1. Generates API keys using random, hashlib and base64 modules.
2. Inserts generated API keys into MongoDB and create an API key pool.
3. Enables clients to ask for an API key, mark the returned API key as used.
4. All subsequent API key requests must not return used API keys from the pool.

Usages:
1. As a module
==============
import api_key_gen
keygen = api_key_gen.APIKeyGenerator()
keygen.create_pool(100)

for x in range(1, 11):
    key = keygen.get_key() # throws error if key pool is exhausted

2. As command line tool
=======================
create api key pool of default size 10
$ python api_key_gen.py

change default pool size
$ python api_key_gen.py -s 100

get key from pool (throws error if key pool is exhausted)
$ python api_key_gen.py -g
"""


__author__ = 'Rajendra Kumar Uppal'
__copyright__ = "Copyright 2015, Rajendra Kumar Uppal"
__credits__ = ["Rajendra Kumar Uppal", "Rich Atkinson"]
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

    def update(self, api_key):
        self.collection.update_one({'key': api_key['key']}, {'$set': {'used': api_key['used']}})


class APIKeyGenerator(object):
    def __init__(self):
        self.api_key_db = APIKeyDatabase()

    def create_pool(self, size):
        for x in range(1, size + 1):
            key = self.generate()
            self.api_key_db.insert(key)

    def get_key(self):
        keys = self.api_key_db.get()
        for key in keys:
            if key['used'] == 'no':
                key['used'] = 'yes'
                self.api_key_db.update(key)
                return key['key']

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

    def get_keys(self):
        return self.api_key_db.get()


def main():
    arg_parser = argparse.ArgumentParser(description='Enter command line arguments.')
    arg_parser.add_argument('-s', '--pool_size', help='Enter API key pool size, default is 10.')
    arg_parser.add_argument('-g', '--get_key', help='Returns a newly generated key.')
    args = arg_parser.parse_args()

    pool_size = args.pool_size
    global APIKEY_POOL_SIZE
    if pool_size:
        APIKEY_POOL_SIZE = int(pool_size)

    api_key_gen = APIKeyGenerator()
    api_key_gen.create_pool(APIKEY_POOL_SIZE)

    for x in range(1, APIKEY_POOL_SIZE + 1):
        print api_key_gen.get_key()

    for key in api_key_gen.get_keys():
        print key

    print api_key_gen.get_key()


if __name__ == '__main__':
    main()
