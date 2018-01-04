import json
import requests
import time
from datetime import datetime
import logging
from utility import readSTR

class Gestione(object):
    def __init__(self):
        '''
        inizializzo la gestione
        '''
        self.playload = {}
        self.dataJson = [] #lista di dict
        self.count = 0

    ######### Metodi Get #################
    def getTimeStamp(self):
        '''
        i = time.time()
        datetime.fromtimestamp(i).strftime("%d%m%y-%H%M%S")
        @return datatime on format ddmmyy-HHMMSS
        '''
        return datetime.fromtimestamp(time.time()).strftime("%d%m%y-%H%M%S")

    ######### Metodi Set #################
    def setLista(self, lista):
        '''
        set lista ritornata da mainSTR
        @param lista:
        @return:
        '''
        self.lista = lista

    def setDataJson(self):
        '''
        set della base per il dataJson, su questa base viene popolato anche il db
        '''
        for s in self.lista:
            idR = time.time()
            data_ins = datetime.fromtimestamp(idR).strftime('%Y-%m-%d %H:%M:%S')
            d = {'dataOra': data_ins,
                 'TipoStr': s['flag'],
                 'TsDevice': s['data'] + '-' + s['orario'],
                 'imei': s['imei'],
                 'Latitudine': s['latitudine'],
                 'Longitudine': s['longitudine'],
                 'EstOvest': s['estOvest'],
                 'NordSud': s['nordSud'],
                 'velocita': s['velocita'],
                 'CoordNewOld': s['coord_nuove'],
                 'CaricaBatteria': s['carica_batteria'],
                 'Future': s['future_espansioni'],
                 'CoordValida': s['CoordValida'],
                 'TsRicezione': s['tsRIcezione'],
                 'FlagRecDuplicato': s['FlagRecDuplicato'],
                 'FlagStrNonValida': s['FlagStrNonValida']}
            # time.sleep(0.1)
            self.dataJson.append(d)
            self.count = self.count + 1

    def setPlayload(self):
        '''
        set self.playload
        '''
        self.playload.update({'TsInvio': self.getTimeStamp(), 'NumElementi': self.count})

    def sendJson(self):
        '''
        invio i dati al server json
        '''
        # data_json = json.dump(self.dataJson)
        self.playload['Elementi'] = self.dataJson
        url = 'http://www.sopla.com/device/api/Device/DevicePosition'
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(self.playload), headers=headers)

    def validazione(self, stringaPic, tsRIcezione):
        '''
        avvio esecuzione
        @param stringaPic:
        @param tsRIcezione:
    	@param db:
        @return:
        '''
        self.playload = {}
        self.dataJson = []
        self.count = 0

        self.setLista(readSTR(stringaPic, tsRIcezione))
        self.setDataJson()  # set dati per db e corpo json
        self.setPlayload()  # set playload per json

        #self.sendJson()  # invio i dati a json
