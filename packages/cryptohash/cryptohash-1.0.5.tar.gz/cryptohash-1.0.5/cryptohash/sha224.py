import hashlib

def sha224(string):
	result = hashlib.sha224(string.encode())
	return result.hexdigest()
