#!/usr/bin/env python

import multiprocessing
import socket
import time
import logging
import select
import Queue
import sys
from db_model import *
from gestione import Gestione
from ConfigParser import SafeConfigParser

#---esempio stringa
#320021716520412345678901234542.123456E123.123456N12.34NS66666666666
def setParamiter(fileParser = '/home/marco/sviluppo/sopla/test/codice/socket/paramiter.ini'):
    param={}
    config = SafeConfigParser()
    config.read(fileParser)

    param['host'] = config.get('server', 'host')
    param['port'] = config.get('server', 'port')
    param['path_log'] = config.get('server', 'path_log')
    param['file_log'] = config.get('server', 'file_log')

    return param

def insertData(data,tsRicezione):
    ges = Gestione()
    ges.validazione(data,tsRicezione)
    ListaOfDict = ges.dataJson

    del ges #disctruggo l'oggetto


    TestS.insert_many(ListaOfDict).execute()
    #-----inserire la connessione al json-----

def handle(connection, address):
    '''

    :param connection:
    :param address:
    :return:
    '''

    #la connessione al db e' stabilita automaticamente all'import del db_model

    tsRIcezione =''

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))
    try:
        logger.debug("Connected %r at %r", connection, address)
        while True:
            data = connection.recv(1024)
            if data == "":
                logger.debug("Socket closed remotely")
                break
            logger.debug("Received data %r", data)
            #connection.sendall(data)
            #logger.debug("Sent data")
            #message_queues[s].put(data)


            tsRIcezione = time.strftime("%d%m%y-%H%M%S")
            #logger.info('SCK:: RCV - data {0} value {1}'.format(tsRIcezione,stringaPic))

            #----------------------invio i dati al gestoreDB----------------------------------------------------
            insertData(data,tsRIcezione)
            # -------------------------------------gestoreDB----------------------------------------------------


    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        connection.close()

    
class Server(object):
    def __init__(self, hostname, port):
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port

    def start(self):
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

if __name__ == '__main__':
    print("Start Server")
    param = setParamiter()
    hostname = socket.gethostname()
    #IP = socket.gethostbyname(hostname)
    #PORT = 8003
    IP = param['host']
    PORT = int(param['port'])
    server = Server(IP, PORT)

    PATH_LOG = param['path_log'] #'/home/cloud/sock/log/'
    FILE_LOG = param['file_log'] #'socket_8003.log'

    logfile = PATH_LOG + FILE_LOG
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    try:
        logger.info('SOCKET OK' )
        server.start()
    except Exception,e:
        print str(e)
        logger.error('Errore inizializzazione socket')
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()

logging.info("All done")

