import os
import time
import struct
import base64
from Crypto.Cipher import AES
from Crypto import Random
from pathlib import Path
from enckey import BLOCK_SIZE
from enckey import PAD,UNPAD
from enckey import DATA_KEY_SIZE
from enckey import ZERO_IV
from enckey.key import Key


class Enckey:

	home = str(Path.home())

	keys_file = home + '/keys.txt'
	
	__key = ''
	
	cipher = []

	def __init__(self):
		flag = False
		while not flag:
			input_key = input('Please enter your master key:\n')
			flag = self.set_key(input_key)
		print('Your cipher will be saved in \''+self.keys_file+'\'')

	
	def set_key(self, input_key):
		input_key = input_key.encode('utf-8')
		if len(input_key) < 6 or len(input_key) > 16:
			print('The key must be longer than 6 bytes and shorter than 16 bytes.')
			return False
		input_key = PAD(input_key)
		self.__key = input_key
		print('Setting key succeeded!')
		return True

	def set_keys_file(self, location):
		if os.path.isfile(location):
			self.keys_file = location
			print('Setting keys file succeeded,your current keys file location is \'' + self.keys_file + '\'')
		else:
			print('Setting keys file failed,please make sure your file \'' + location + '\' exist.' )
			print('Your current keys file location is \'' + self.keys_file + '\'')

	def encrypt(self, data, descrypt='new key'):
		# padding
		data = data.encode('utf-8')
		data = PAD(data)

		# encrypt plaintext using random key, _iv size is 16bytes
		data_key = Random.new().read(DATA_KEY_SIZE)
		_iv = Random.new().read(BLOCK_SIZE)
		aes = AES.new(data_key, AES.MODE_CBC, _iv)
		data_cipher = aes.encrypt(data) 

		# encrypt plaintext key using master key
		aes = AES.new(self.__key, AES.MODE_CBC, ZERO_IV)
		data_key_cipher = aes.encrypt(data_key)

		# construct cipher
		header = struct.pack('>h', len(data_key_cipher)) + data_key_cipher + _iv
		completed_cipher = header + data_cipher
		cipher_str = base64.b64encode(completed_cipher).decode('utf-8')

		# write cipher to local file
		now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
		with open(self.keys_file,'a') as f:
			f.write(now + '\t')
			f.write(descrypt + '\t')
			f.write(cipher_str + '\n')
			f.flush()
			f.close()

		return completed_cipher

	def load_cipher(self, output=False):
		self.cipher.clear()
		i = 0
		with open(self.keys_file, 'r') as f:
			for line in f:
				key_list = line.strip().split('\t')
				key = Key(key_list[0], key_list[1], key_list[2])
				self.cipher.append(key)
		if output:
			for ct in self.cipher:
				print(ct.get_create_time(), end = ' ')
				print(ct.get_description(), end = '\t')
				print(ct.get_cipher())

		return self.cipher

	def decrypt(self, cipher):
		cipher = base64.b64decode(cipher.encode('utf-8'))
		try:
			data_key_cipher, _iv, data_cipher = self.__extract(cipher)	

			aes = AES.new(self.__key, AES.MODE_CBC, ZERO_IV)
			data_key = aes.decrypt(data_key_cipher)

			aes = AES.new(data_key, AES.MODE_CBC, _iv)
			data = UNPAD(aes.decrypt(data_cipher).decode('utf-8'))

			return data
		except Exception as e:
			print('Decryption with exception: ' + str(e))

		

	def __extract(self, cipher):
		'''extract data key,data key cipher,iv and data cipher'''
		try:
			index = 0
			data_key_cipher_len = struct.unpack('>h', cipher[index:index+2])[0]
			index += 2
			data_key_cipher = cipher[index:index+data_key_cipher_len]
			index += data_key_cipher_len
			_iv = cipher[index:index+BLOCK_SIZE]
			index += BLOCK_SIZE
			data_cipher = cipher[index:]
			return data_key_cipher, _iv, data_cipher
		except Exception as e:
			print('Your cipher is corrupted. With exception: ' + str(e))
			raise e
			
	def change_key(self, new_key):
		now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
		ciphers = self.load_cipher()
		plains = []
		for cipher in ciphers:
			decrypt_str = self.decrypt(cipher.get_cipher())
			plain = Key(now, cipher.get_description(), decrypt_str)
			plains.append(plain)
		flag = self.set_key(new_key)
		if not flag:
			print('Change key failed.')
			return
		with open(self.keys_file, 'w') as f:
			for plain in plains:
				self.encrypt(plain.get_cipher(), plain.get_description())
				

