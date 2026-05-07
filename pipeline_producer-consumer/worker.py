import multiprocessing #-
import zmq, time, pickle, sys, random #-
#-

NWORKERS = 10 #-

def worker(id):
  context = zmq.Context()
  socket  = context.socket(zmq.PULL)      # create a pull socket
  socket.connect("tcp://localhost:12345") # connect to the producer
  thisworker = format(id,'03d') #-

  while True:
    print("Worker " + thisworker + " wants work") #-    
    work = pickle.loads(socket.recv())     # receive work from a source
    print("Worker " + thisworker + " gets   " + format(work,'03d')) #-
    time.sleep(work)                       # pretend to work

