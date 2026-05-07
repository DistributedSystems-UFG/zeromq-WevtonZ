import multiprocessing
import zmq, time, pickle, sys, random
from constPipe import * #-

def producer(id, port):
	context = zmq.Context()              
	socket  = context.socket(zmq.PUSH)        # create a push socket
	socket.bind("tcp://*:"+port)                             # bind socket to address
	
	for i in range(100):                  # generate 100 workloads
		workload = random.randint(1, 100)   # compute workload
		print ("Producer " + id + " sending workload item of size " + str(workload))
		socket.send(pickle.dumps(workload)) # send workload to worker

if sys.argv[1] == '1':
	producer('1', PORT1)
elif sys.argv[1] == '2':
	producer('2', PORT2)
