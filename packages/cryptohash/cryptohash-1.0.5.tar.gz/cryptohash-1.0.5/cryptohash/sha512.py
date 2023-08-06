import hashlib

def sha512(string):
	result = hashlib.sha512(string.encode())
	return result.hexdigest()
