'''
classe che viene chiamata dal socket per eseguire l'aggiornameto sul db ed inviare i dati su json
'''
import json
import requests
import time
from db import Databases
from datetime import datetime
#import urllib2
import logging
from mainSTR import readSTR

class Gestione(object):
    def __init__(self):
        '''
        inizializzo la gestione
        @param lista: list delle stringhe len(70) con flag duplicato e strvalida settati
        @param tsRIcezione dataOra di ricezione
        '''
        #self.lista = lista          #lista di dict
        self.playload = {}
        self.dataJson = []
        self.count = 0

    ######### Metodi Get #################
    def getTimeStamp(self):
        '''
        i = time.time()
        datetime.fromtimestamp(i).strftime("%d%m%y-%H%M%S")
        :return datatime on format ddmmyy-HHMMSS
        '''
        return datetime.fromtimestamp(time.time()).strftime("%d%m%y-%H%M%S")

    ######### Metodi Set #################
    def setLista(self,lista):
        '''
        set lista ritornata da mainSTR
        :param lista:
        :return:
        '''
        self.lista=lista

    def setDataJson(self):
        '''
        set della base per il dataJson, su questa base viene popolato anche il db
        '''
        for s in self.lista:
            d={'IdRecord': time.time(),
               'TipoStr':s['flag'],
               'TsDevice':s['data']+'-'+s['orario'],
               'Imei':s['imei'],
               'Latitudine': s['latitudine'],
               'Longitudine': s['longitudine'],
               'EstOvest':s['estOvest'],
               'NordSud':s['nordSud'],
               'Velocita':s['velocita'],
               'CoordNewOld':s['coord_nuove'],
               'CaricaBatteria':s['carica_batteria'],
               'Future':s['future_espansioni'],
               'CoordValida':s['CoordValida'],
               'TsRicezione':s['tsRIcezione'],
               'FlagRecDuplicato':s['FlagRecDuplicato'],
               'FlagStrNonValida': s['FlagStrNonValida']}
	    #time.sleep(0.1)				
            self.dataJson.append(d)
            self.count = self.count + 1

    def setPlayload(self):
        '''
        set self.playload
        '''
        self.playload.update({'TsInvio':self.getTimeStamp(), 'NumElementi': self.count })
    ######### END #################

    def sendJson(self):
        '''
        invio i dati al server json
        '''
        #data_json = json.dump(self.dataJson)
        self.playload['Elementi'] = self.dataJson
        url = 'http://www.sopla.com/device/api/Device/DevicePosition'
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(self.playload), headers=headers)
	#logger.info("JSON::status code {0} - answer string".format(r.status,r.json()))
	#print("DataJson: {0}".format(self.dataJson))
	#print("JSON STATUS")
	#print r.status_code
	#print r.json()
        #da verificare la risposta

    #def main(self):
        #logging.info('SCK:: start Gestione.main')
        #self.setDataJson()  #setto il campo dataJson con i dati ricevuti
        #self.setPlayload()  # costruisco il playLoad per il json

    def connessioneDB(self):
        '''
        connessione al database
        :return:
        '''
        #self.db = Databases(self.dataJson)
        self.db = Databases()
        self.db.connetti()

    def run(self,stringaPic,tsRIcezione,db):
        '''
        avvio esecuzione
        :param stringaPic:
        :param tsRIcezione:
        :return:
        '''
        self.playload = {}
        self.dataJson = []
        self.count = 0
        
	self.setLista(readSTR(stringaPic, tsRIcezione))
        self.setDataJson()   #set dati per db e corpo json
        self.setPlayload()   #set playload per json
	#print("Lista stringhe {0}".format(self.dataJson))
	#print help(db)
        #self.db.insertDb()  #insert on db
	db.insertDb(self.dataJson)
        self.sendJson()     #invio i dati a json


if __name__ == '__main__':
    stringaPic='&320021716520412345678901234542.123456E123.123456N12.34NS66666666666'
    tsRIcezione = time.strftime("%d%m%y-%H%M%S")
    ges = Gestione()
    ges.run(stringaPic,tsRIcezione)
    
