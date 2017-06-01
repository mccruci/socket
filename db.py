import MySQLdb
import logging
from ConfigParser import SafeConfigParser

class Databases(object):

    __INSERT_DB="INSERT INTO apparati (idRecord,TipoStr,TsDevice,imei,Latitudine,Longitudine,EstOvest,NordSud,velocita,CoordNewOld,CoordValida,CaricaBatteria,Future,TsRicezione,FlagRecDuplicato,FlagStrNonValida) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    def __init__(self):
        """
        inizializo l'oggetto e setto il parametro listaDiDict
        """
        #self.listaDiDict = lista

    def connetti(self, fileParser='/home/cloud/sock/paramiter.ini'):
        """
        connessione al databases in base ai parametri ricevuti
        """
        config = SafeConfigParser()
        config.read(fileParser)
        self.host = config.get('default', 'database_host')
        self.user = config.get('default', 'database_user')
        self.passwd = config.get('default', 'database_password')
        self.dbName = config.get('default', 'database_name')

        try:
            self.db = MySQLdb.connect(self.host, self.user, self.passwd, self.dbName)
            self.cur = self.db.cursor()
            logging.info('SCK:: connessione db')
        except MySQLdb.Error, e:
            logging.error("SCK::ERROR connessione db: %s", e)

    def close(self):

        try:
            self.cur.close()
            self.db.close()
        except MySQLdb.Error, e:
            logging.error("SCK::ERROR close db: %s", e)

    def insertDb(self,lista):
        """
        insert into nel database
        """
        item=[]
        for row in lista: #self.listaDiDict:
            item.append((row['IdRecord'],row['TipoStr'],row['TsDevice'],row['Imei'],row['Latitudine'],row['Longitudine'],row['EstOvest'],row['NordSud'],row['Velocita'],row['CoordNewOld'],row['CoordValida'],row['CaricaBatteria'],row['Future'],row['TsRicezione'],row['FlagRecDuplicato'],row['FlagStrNonValida']))
        try:
            self.cur.executemany(self.__INSERT_DB, item)
            self.db.commit()
        except MySQLdb.Error, e:
	    print("ECCEZIONE {0}, --LISTA-- = {1}".format(e,lista))
            logging.error("SCK::Errore insertDb")

