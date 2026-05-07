import multiprocessing #-
import zmq, time, pickle, sys, random #-
from constPipe import PORT1
#-

def producer():
  context = zmq.Context()              
  socket  = context.socket(zmq.PUSH)      # create a push socket
  socket.bind(f"tcp://*:{PORT1}")    # bind socket to address
  
  while True:
    workload = random.randint(1, 100)     # compute workload
    print("Produced workload", format(workload,'03d')) #-
    socket.send(pickle.dumps(workload))   # send workload to worker
    time.sleep(workload/10)         # balance production by waiting 

if __name__ == "__main__":
  producer()