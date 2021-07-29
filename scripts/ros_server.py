#!/usr/bin/env python
import socket
import sys
import rospy
import time
from std_srvs.srv import Trigger, TriggerResponse

#this node is a ros server and a socket client, this node runs on amir2, state machine will trigger this and then
#socket client will send a request to socket server on amir
class ros_server:
	def __init__(self, HOST, PORT, cmd):
		self.HOST = HOST
		self.PORT = PORT
		self.cmd = cmd
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		#keep try connect until succeed
		connected = False
		while not connected: 
			try:
				self.s.connect((self.HOST,self.PORT))
				connected = True
			except Exception as e:
				pass

	def trigger_response(self,request):
		self.send_cmd()
		return TriggerResponse(success=True, message='I am leaving')

	def trigger_server(self):
		my_service = rospy.Service('/amir2_leave_service', Trigger, self.trigger_response)
		rospy.spin()
	
	def send_cmd(self):
		try:
			self.s.send(self.cmd)
		except:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((self.HOST, self.PORT))
			self.s.send(cmd)


if __name__ == "__main__":
	rospy.init_node('trigger_amir2_server')	
	
	host = rospy.get_param('/host', 'localhost')
	port = rospy.get_param('/port', 8000)
	signal = rospy.get_param('/signal', 'AMIR_GOGO')
	
	server = ros_server(host, port, signal)
	server.trigger_server()

	