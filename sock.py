import socket
import time
import logging
import select
import Queue
import sys
from gestione import Gestione
from db import Databases

#from lettura_str import readSTR

#---esempio stringa
#320021716520412345678901234542.123456E123.123456N12.34NS66666666666

def main():
	print("start socket srv")

	hostname = socket.gethostname()
	IP = socket.gethostbyname(hostname)
	PORTA = 8003
	
	PATH_LOG = '/home/cloud/sock/log/'
	FILE_LOG = 'socket_8003.log'

	logfile = PATH_LOG + FILE_LOG
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	fh = logging.FileHandler(logfile)
	fh.setLevel(logging.DEBUG)

	formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s - %(message)s')
	fh.setFormatter(formatter)

	logger.addHandler(fh)

	try:
		server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		server.setblocking(0)
		server.bind((IP,PORTA))
		server.listen(5)

		logger.info('SOCKET OK' )
	except:
		logger.error('Errore inizializzazione socket')
		exit(1)

	inputs = [server]
	outputs = []
	message_queues = {}
	stringaPic=''

	#inizializo gestione e contestualmente il db, lascio la connessione aperta
	ges=Gestione()
	'''
	sono abilitati dalla gestione
        db = Databases()
        db.connetti()
	'''
	ges.connessioneDB()
	tsRIcezione =''


	while inputs:
		#print >>sys.stderr, '\nwarning for the next event'
		readable, writeable, exceptional = select.select(inputs, outputs, inputs, 20)

		for s in readable:
			if s is server:
				connection, client_address = s.accept()
				#print >>sys.stderr, 'new connection from', client_address  #il client stabilisce la connessione
				connection.setblocking(0)
				inputs.append(connection)
				message_queues[connection] = Queue.Queue()

			else:
				data = s.recv(1024)
				if data:
					#print >>sys.stderr, 'received "{0}" from {1}'.format(data, s.getpeername())  #il client invia i dati
					message_queues[s].put(data)
					stringaPic=data
            				tsRIcezione = time.strftime("%d%m%y-%H%M%S")
                        		logger.info('SCK:: RCV - data {0} value {1}'.format(tsRIcezione,stringaPic))

					#print("stringa {0}".format(stringaPic))
					if s not in outputs:
						outputs.append(s)
				else:
					#print >>sys.stderr, 'closing', client_address, 'after reading no data'  #non e' stato ricevuti nessun dato
					if s in outputs:
            		    			outputs.remove(s)
            				inputs.remove(s)
            				s.close()
            				del message_queues[s]
            				ges.run(stringaPic,tsRIcezione,)
	print("uscita")
if __name__ == '__main__':
	main()

