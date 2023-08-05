from Crypto.Cipher import AES

name = "enckey"

BLOCK_SIZE = AES.block_size

PAD = lambda x: x + (BLOCK_SIZE - len(x) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(x) % BLOCK_SIZE).encode('utf-8')

UNPAD = lambda x: x[0:len(x)-ord(x[len(x)-1])]

DATA_KEY_SIZE = 32

ZERO_IV = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
