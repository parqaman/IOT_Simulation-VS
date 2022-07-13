import sys

COORDINATOR_IP = '172.30.0.5'
COORDINATOR_PORT = 9090

sys.path.append('gen-py')

# Example files
from MyDBService import *
from MyDBService.ttypes import *

# Thrift files
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

def create_thrift_client(DB_IP, DB_PORT):
    # Init thrift connection and protocol handlers
    tsocket = TSocket.TSocket( DB_IP , DB_PORT)
    transport = TTransport.TBufferedTransport(tsocket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = MyDBService.Client(protocol)

    return (client, transport)


class Coordinator:
    def __init__(self):
        # Pushing both DB address and port
        self.DB_LIST = []
        self.DB_LIST.append(('172.30.0.8', 9090))
        self.DB_LIST.append(('172.30.0.9', 9090))

        self.Thrift_Client_Transport = []
        for db_addr in self.DB_LIST:
            # Pushing and creating thrift client for communication between each DB
            (thrift_client, thrift_transport) = create_thrift_client(db_addr[0], db_addr[1])
            self.Thrift_Client_Transport.append((thrift_client, thrift_transport))

    # Checking all status of DBs
    # All DB must be ready, otherwise abort transaction
    def check_all_db(self):
        for thrift_cli, thrift_trans in self.Thrift_Client_Transport:
            stat = False
            try:
                thrift_trans.open()
                stat = thrift_cli.status_check()
                thrift_trans.close()
            except:
                print("A DB is not available")
                if stat != True:
                    return False
        print("All DB is available")
        return True

    def create(self, in_data):
        stat = self.check_all_db()
        if stat != True:
            return False

        # Calling create function of both DB (Commiting action in both DB)
        for thrift_cli, thrift_trans in self.Thrift_Client_Transport:
            thrift_trans.open()
            thrift_cli.create(in_data)
            thrift_trans.close()
        return True

    def read(self):
        # Taking only data from one of the DB, since they are the same
        thrift_cli, thrift_trans = self.Thrift_Client_Transport[0]
        thrift_trans.open()
        content = thrift_cli.read()
        thrift_trans.close()
        return content

    def update(self, index, new_entry):
        stat = self.check_all_db()
        if stat != True:
            return False

        # Calling update function of both DB (Commiting action in both DB)
        for thrift_cli, thrift_trans in self.Thrift_Client_Transport:
            thrift_trans.open()
            thrift_cli.update(index, new_entry)
            thrift_trans.close()
        return True

    def delete(self, index):
        stat = self.check_all_db()
        if stat != True:
            return False

        # Calling delete function of both DB (Commiting action in both DB)
        for thrift_cli, thrift_trans in self.Thrift_Client_Transport:
            thrift_trans.open()
            thrift_cli.delete(index)
            thrift_trans.close()
        return True
            

if __name__ == '__main__':
    # set handler to our thrift implementation
    handler = Coordinator()

    processor = MyDBService.Processor(handler)
    transport = TSocket.TServerSocket( COORDINATOR_IP, COORDINATOR_PORT )
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # set thrift server
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

    print('Database Coordinator server started...')
    server.serve()