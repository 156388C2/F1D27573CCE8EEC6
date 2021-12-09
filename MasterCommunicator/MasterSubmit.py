

import time

import random
import socket
import sys

import Common

HOST_NAME = Common.HOST_NAME
PORT_NUMBER_MASTER = 58643

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST_NAME, PORT_NUMBER_MASTER))

	question = bytes.fromhex(sys.argv[1])
	Common.send_object(s, question)
	answer = Common.recv_object(s)
	assert Common.is_in_search_space(answer)
	assert question == Common.MD5(answer)
	print(answer.decode())
	
	