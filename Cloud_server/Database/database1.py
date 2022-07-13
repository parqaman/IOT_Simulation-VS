import sys
# your gen-py dir

DATABASE_IP = '172.30.0.8'
DATABASE_PORT = 9090

sys.path.append('gen-py')

# Example files
from MyDBService import *
from MyDBService.ttypes import *

# Thrift files
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class DB:
    def __init__(self):
        self.the_list = []

    def create(self, in_data):
        self.the_list.append(in_data)

    def read(self):
        return self.the_list

    def update(self, index, new_entry):
        self.the_list[index] = new_entry

    def delete(self, index):
        del self.the_list[index]

    def status_check(self):
        return True

if __name__ == '__main__':
    # set handler to our thrift implementation
    handler = DB()

    processor = MyDBService.Processor(handler)
    transport = TSocket.TServerSocket(DATABASE_IP, DATABASE_PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # set thrift server
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

    print('Database 1 server started...')
    server.serve()