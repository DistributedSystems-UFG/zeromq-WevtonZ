import multiprocessing #-
import zmq
from time import sleep #-

def client():
  context = zmq.Context()
  socket  = context.socket(zmq.REQ)       # create request socket

  socket.connect("tcp://34.228.41.207:5679") # block until connected
  socket.send(b"Hello world")             # send message
  message = socket.recv()                 # block until response
  socket.send(b"STOP")                    # tell server to stop
  print(message.decode())                 # print result

client()