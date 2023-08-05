from setuptools import setup

setup(
	name = 'enckey',
	version = '0.0.1',
	description = 'a tools to encrypt personal private keys',
	packages = ['enckey'],
	package_data = {'enckey':['resource/keys.txt']},
	include_package_data = True,
	license = 'LICENSE.txt',
	author = 'hammo',
	author_email = 'hammo@gmail.com',
	url = 'https://github.com/maxsuren/enckey'
)
