# api-key-generator
Simple API key generator using Python

### Development Environment
OS: Windows 8.1 64-bit

Tools:
* Python 2.7.9
* MongoDB 3.0.2
( Download 64-bit installer from https://www.mongodb.org/downloads )
* pymongo ( pip install pymongo )
* argparse
* Git

### Usage

You can use this application both as a module and as a command line utility.

##### As a module
```python
import api_key_gen
apikey = api_key_gen.APIKeyGenerator()
key = apikey.generate()
print key
```

##### As command line utility

Run following command for help
```
$ python api_key_gen.py -h or --help
```

Create pool:
```
$ python api_key_gen.py -s 100
```
-s pool size, default is 10
