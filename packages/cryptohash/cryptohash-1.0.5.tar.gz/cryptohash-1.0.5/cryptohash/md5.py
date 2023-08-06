import hashlib

def md5(string):
	result = hashlib.md5(string.encode())
	return result.hexdigest()
