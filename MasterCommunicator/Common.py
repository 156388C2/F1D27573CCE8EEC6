

import hashlib
import pickle
import random

HOST_NAME = 'master.gnhfp3.ch-geni-net.instageni.colorado.edu'

def sample_uniform_search_space():
	x = ''.join([chr(ord('A') + random.randint(0, 25)) for _ in range(5)]).encode()
	return x

def is_in_search_space(x):
	if not isinstance(x, bytes):
		return False
	if len(x) != 5:
		return False
	for c in x:
		if c < ord('A') and ord('Z') < c:
			return False
	return True

def MD5(x):
	assert isinstance(x, bytes)
	y = hashlib.md5(x).digest()
	return y

def send_object(s, obj):
	content = pickle.dumps(obj)
	header = len(content).to_bytes(4, 'big')
	
	assert len(header) == s.send(header)
	assert len(content) == s.send(content)

def recv_object(s):
	# Read header
	header = s.recv(4)
	if len(header) != 4:
		raise RuntimeError
	line_length = int.from_bytes(header, 'big')

	# Read payload
	line = bytes()
	while len(line) < line_length:
		content = s.recv(line_length - len(line))
		line += content[:min(len(content), line_length - len(line))]
	received_object = pickle.loads(line)

	return received_object

