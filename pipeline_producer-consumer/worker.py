import multiprocessing #-
import zmq, time, pickle, sys, random #-
from constPipe import NWORKERS, SRC1, PORT1
#-

def worker():
  context = zmq.Context()
  socket  = context.socket(zmq.PULL)      # create a pull socket
  socket.connect(f"tcp://{SRC1}:{PORT1}") # connect to the producer
  thisworker = format(id,'03d') #-

  while True:
    print("Worker " + thisworker + " wants work") #-    
    work = pickle.loads(socket.recv())     # receive work from a source
    print("Worker " + thisworker + " gets   " + format(work,'03d')) #-
    time.sleep(work)                       # pretend to work

if __name__ == "__main__":
  worker()