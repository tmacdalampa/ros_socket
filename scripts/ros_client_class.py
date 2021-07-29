#!/usr/bin/env python
import socket
import sys
import rospy
from thread import *
from std_srvs.srv import Trigger, TriggerRequest

#this node is a ros client and a socket server, this node runs on amir, after receive socket data "AMIR_GOGO"
#the ros client will call test_server trigger state mahine on amir start

class ros_client:
	def __init__(self, HOST, PORT, cmd):
		self.HOST = HOST
		self.PORT = PORT
		self.cmd = cmd
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print('Socket created')

		try:
			self.s.bind((self.HOST, self.PORT))
		except socket.error , msg:
			print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
			sys.exit()

		print('Socket bind complete')

		self.s.listen(10)
		print('Socket now listening')

	def clientthread(self, conn,clientaddress):
		while True:
			data = conn.recv(1024)
			reply = 'server reply:\t' + data
			print(clientaddress+'\t'+'say:'+data)
			sos_service = rospy.ServiceProxy('/amir_start_service', Trigger)
			if data == self.cmd:
				sos = TriggerRequest()
				result = sos_service(sos)
				print(result)
			if not data:
				break
			conn.sendall(reply)

		conn.close()

if __name__ == "__main__":

	rospy.init_node('trigger_amir2_client')
	rospy.wait_for_service('/amir_start_service')
	host = rospy.get_param('/host', 'localhost')
	port = rospy.get_param('/port', 8000)
	signal = rospy.get_param('/signal', 'AMIR_GOGO')
	client = ros_client(host, port, signal)
	
	while 1:
		conn, addr = client.s.accept()
		clientaddress = addr[0]+':'+str(addr[1])
		print('Connected with ' + clientaddress)
		start_new_thread(client.clientthread,(conn,clientaddress))
	client.s.close()

