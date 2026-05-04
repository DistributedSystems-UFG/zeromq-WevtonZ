import multiprocessing #-
import zmq
from time import sleep #-

def server():
  context = zmq.Context()
  socket  = context.socket(zmq.REP)       # create reply socket
  socket.bind("tcp://*:5679")            # bind socket to address

  while True:
    message = socket.recv()               # wait for incoming message
    if not "STOP" in str(message):        # if not to stop...
      reply = str(message.decode())+'*'   # append "*" to message
      socket.send(reply.encode())         # send it away (encoded)
    else:                         
      break    

server()