import hashlib

def sha256(string):
	result = hashlib.sha256(string.encode())
	return result.hexdigest()
