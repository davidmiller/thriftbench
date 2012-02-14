"""
server.py

A simple Thrift server in python for benchmarking purposes
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'gen-py'))

from bench import Bencher

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer, TProcessPoolServer

class BenchHandler(object):

  def ping(self):
      return "pong"

  def sortset(self, integers):
      integers = list(set(integers))
      integers.sort()
      return integers

def main():
    """
    Serve indefinitely
    """
    handler = BenchHandler()
    processor = Bencher.Processor(handler)
    transport = TSocket.TServerSocket(port=30303)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # Our server implementations - comment out for quick swapping
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    #server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    #server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    #server = TServer.TForkingServer(processor, transport, tfactory, pfactory)
    #server = TProcessPoolServer.TProcessPoolServer(processor, transport, tfactory, pfactory)
    print "Starting %s server on port 30303... " % server.__class__
    server.serve()

if __name__ == '__main__':
    main()

