class Key:
	def __init__(self, time, msg, cipher):
		self.create_time = time
		self.description = msg
		self.cipher = cipher

	def get_create_time(self):
		return self.create_time

	def get_description(self):
		return self.description

	def get_cipher(self):
		return self.cipher