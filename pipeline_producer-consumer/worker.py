import multiprocessing #-
import zmq, time, pickle, sys, random #-
from constPipe import SRC1, PORT1
#-

def worker(id):
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
  if(len(sys.argv) > 1):
    meu_id = int(sys.argv[1])
  else:
    meu_id = random.randint(1,1000)
  worker(meu_id)