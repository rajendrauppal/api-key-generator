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


import random
import hashlib
import base64


def main():
    pass


if __name__ == '__main__':
    main()
