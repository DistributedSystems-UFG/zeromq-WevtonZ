import multiprocessing #-
import zmq
from time import sleep #-
import zmq_client
import zmq_server

if __name__ == "__main__": #-
  s = multiprocessing.Process(target=server) #-
  c = multiprocessing.Process(target=client) #-
#-
  s.start() #-
  sleep(2) #-
  c.start() #-
  c.join() #-
  s.join() #-
