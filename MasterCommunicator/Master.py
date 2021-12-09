

import time

import select
import socket
import threading

import Common

HOST_NAME = Common.HOST_NAME
PORT_NUMBER_WORKER = 58642
PORT_NUMBER_MASTER = 58643
NUM_MAX_INCOMING_CONNECTIONS = 5

questions_to_answer = dict()
questions_to_answer_lock = threading.Lock()

def worker_recv_thread_target(clientsocket):
	try:
		while True:
			received_object = Common.recv_object(clientsocket)
			if received_object is not None:
				question = Common.MD5(received_object)
				with questions_to_answer_lock:
					assert question in questions_to_answer
					questions_to_answer[question] = received_object
					print('Worker sent answer:', question, received_object)
	except:
		pass

def worker_send_thread_target(clientsocket):
	try:
		while True:
			with questions_to_answer_lock:
				needles = {
					question
					for question in questions_to_answer
					if questions_to_answer[question] is None
				}
				Common.send_object(clientsocket, needles)
			time.sleep(1)
	except:
		pass

def master_thread_target(clientsocket):
	question = Common.recv_object(clientsocket)
	
	with questions_to_answer_lock:
		if question not in questions_to_answer:
			questions_to_answer[question] = None
	
	while True:
		with questions_to_answer_lock:
			if questions_to_answer[question] is not None:
				Common.send_object(clientsocket, questions_to_answer[question])
				break
		time.sleep(1)

if __name__ == '__main__':
	sw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sw.bind((HOST_NAME, PORT_NUMBER_WORKER))
	sw.listen(NUM_MAX_INCOMING_CONNECTIONS)
	
	sm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sm.bind((HOST_NAME, PORT_NUMBER_MASTER))
	sm.listen(NUM_MAX_INCOMING_CONNECTIONS)

	while True:
		inputs = [sw, sm]
		readable, writable, exceptional = select.select(inputs, [], inputs)
		
		for s in readable:
			if s is sw:
				(clientsocket, (client_ip, client_port)) = s.accept()
				
				print()
				print('Worker connected: {:s}:{:d}'.format(client_ip, client_port))
				
				worker_send_thread = threading.Thread(target = worker_send_thread_target, args = (clientsocket,))
				worker_send_thread.start()
				
				worker_recv_thread = threading.Thread(target = worker_recv_thread_target, args = (clientsocket,))
				worker_recv_thread.start()
			elif s is sm:
				(clientsocket, (client_ip, client_port)) = s.accept()
				
				print()
				print('Master connected: {:s}:{:d}'.format(client_ip, client_port))
				
				master_thread = threading.Thread(target = master_thread_target, args = (clientsocket,))
				master_thread.start()
		
		for s in exceptional:
			print('Exceptional:', s)
			raise RuntimeError

