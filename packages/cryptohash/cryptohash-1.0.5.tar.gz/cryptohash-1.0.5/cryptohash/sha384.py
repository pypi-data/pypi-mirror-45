import hashlib

def sha384(string):
	result = hashlib.sha384(string.encode())
	return result.hexdigest()
