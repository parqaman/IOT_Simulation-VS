import sqlite3
import sys
# your gen-py dir

DATABASE_IP = '172.30.0.5'
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
    def create_table(self, table_name):
        c.execute("""
            CREATE TABLE {} (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                value   INTEGER
            )
        """.format(table_name))
        conn.commit()

    def read_data(self, rows, table_name):
        c.execute("SELECT {} FROM {}".format(rows, table_name))
        datas = c.fetchall()
        data_in_string = ';'.join([str(item) for item in datas])
        return data_in_string

    def insert_data(self, in_data):
        unit = in_data.split(':') # 'T:10-Celc' -> {T, 10-Celc}
        value = unit[1].split('_')[0] # splitted_input[1] = '10-Celc'.split('_') -> {10, Celc}
        c.execute("INSERT INTO {} VALUES (NULL, {})".format(unit[0], value))
        conn.commit()
    
    def delete_data(self, table_name, id):
        c.execute("""
            DELETE FROM {} WHERE id = {}
        """.format(table_name, id))
        conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    c = conn.cursor()

    # set handler to our thrift implementation
    handler = DB()

    processor = MyDBService.Processor(handler)
    transport = TSocket.TServerSocket(DATABASE_IP, DATABASE_PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # set thrift server
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

    print('Database server started...')
    server.serve()