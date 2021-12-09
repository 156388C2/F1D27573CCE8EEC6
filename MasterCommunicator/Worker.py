

import time

import hashlib
import pickle
import random
import socket
import threading

import Common

HOST_NAME = Common.HOST_NAME
PORT_NUMBER_WORKER = 58642

needles = set()
needles_lock = threading.Lock()

hashes_checked = 0

last_hash_time = time.time()
last_hash_number = 0
hash_rate_mean = 0
hash_rate_mean_momentum = 0.99

def communicate_thread_target(s):
	global needles
	
	while True:
		received_object = Common.recv_object(s)
		with needles_lock:
			needles = received_object

def search_thread_target(s):
	global hashes_checked
	global hash_rate_mean
	global last_hash_number
	global last_hash_time
	
	while True:
		# Sleep when there are no needles to find
		with needles_lock:
			len_needles = len(needles)
		if len_needles == 0:
			time.sleep(1)
			print(hashes_checked, 'sleeping')
			continue

		# Check random element of search space
		x = Common.sample_uniform_search_space()
		y = Common.MD5(x)
		
		# Estimate hash rate
		hashes_checked += 1
		if hashes_checked % 10000 == 0:
			instantaneous_hash_rate = (hashes_checked - last_hash_number) / (time.time() - last_hash_time)
			hash_rate_mean = hash_rate_mean_momentum * hash_rate_mean + (1 - hash_rate_mean_momentum) * instantaneous_hash_rate
			last_hash_number = hashes_checked
			last_hash_time = time.time()
			print(hashes_checked, hash_rate_mean)

		with needles_lock:
			if y in needles:
				Common.send_object(s, x)
			len_needles = len(needles)

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST_NAME, PORT_NUMBER_WORKER))

	communicate_thread = threading.Thread(target = communicate_thread_target, args = (s,))
	communicate_thread.start()

	search_thread = threading.Thread(target = search_thread_target, args = (s,))
	search_thread.start()

