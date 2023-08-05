# Enckey

 ![py27][py27] ![py35][py35]

It is really a sufferring thing to memorize tons of keys like your bank key or facebook account key and so on,what's more, most of them need to be updated periodically. However it is not a smart act to just write your keys down on your notebook or smartphone which most people do. In fact, there is no any secure place that you can hide your keys from being spied. So enckey is a python package to solve this anti-human problem. Enckey is based on the commonly used cryptography algorithm AES, it can encrypt the whole keys mentioned above with merely one 128-bit AES key and store them on your disk as cipher. Now you can  feel free to write even hundreds of your keys as cipher on your laptop or smartphone without worrying about the safety, but you only have to remember one single key.

## Install
* Source code  
clone this project, cd to the root directory of enckey, run `install.sh` script to install and `test.sh` to run test
## Usage
``` python
from enckey.enckey import Enckey

client = Enckey()

# client.set_key('88888888') # specify your key, longer than 6 bytes but shorter than 16 bytes
# client.set_keys_file('home/keys.file') # specify your cipher file location, default is '${HOME}/keys.file'

client.encrypt('my_bank_key', 'my_key_description')
# the record in keys.file would be:
# 2018-11-27 22:02	my_key_description	ACDlYglx8j6QYyXoNMmlxwmzwZqz3LW8pThpM01CmSQJKpXExlTc9EhW7k39b1qXLPMpV4pOJkL7hGRzq5SoTIdK

cipher_list = client.load_cipher(output=True) # set output=True will print your cipher records on the console

# ct is a list of the cipher records, each of them includes cipher and description field.
cipher = cipher_list[0].get_cipher()
plain_key = client.decrypt(cipher)
print(plain_key)
# 'my_bank_key'
```

[py27]: https://img.shields.io/badge/python-2.7-ff69b4.svg "python27"
[py35]: https://img.shields.io/badge/python-3.5-red.svg "python35"
