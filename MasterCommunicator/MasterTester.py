

import time

import random
import socket
import sys

import Common

HOST_NAME = Common.HOST_NAME
PORT_NUMBER_MASTER = 58643

if __name__ == '__main__':
	for _ in range(100):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST_NAME, PORT_NUMBER_MASTER))

		x = Common.sample_uniform_search_space()
		question = Common.MD5(x)
		time_start = time.time()
		Common.send_object(s, question)
		answer = Common.recv_object(s)
		time_end = time.time()
		assert answer == x
		print('{!s:s} : {:9.2f}'.format(answer, time_end - time_start))
		sys.stdout.flush()

