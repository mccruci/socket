from counter import Counter
import string


def readSTR(richiesta, tsRIcezione):
    Lista = richiesta.split('&')
    Lista.pop(0)
    lista = validitaLista(Lista)  # validazione lista
    listOfDict = []  # creo la lista di dist vuota
    for s in lista:
        datiDict = {'tsRIcezione': tsRIcezione,
                    'flag': s[:1],
                    'data': s[1:7],
                    'orario': s[7:13],
                    'imei': s[13:28],
                    'latitudine': s[28:37],
                    'estOvest': s[37:38],
                    'longitudine': s[38:48],
                    'nordSud': s[48:49],
                    'velocita': s[49:54],
                    'coord_nuove': s[54:55],
                    'coord_valida': s[55:56],
                    'carica_batteria': s[56:57],
                    'future_espansioni': s[57:67],
                    'FlagStrNonValida': s[67:68],
                    'FlagRecDuplicato': s[68:69], }

        if datiDict['FlagStrNonValida'] == 'S':  # lista valida
            if checkCoord(datiDict['latitudine']) and checkCoord(datiDict['longitudine']):
                datiDict['CoordValida'] = 'S'
            else:
                datiDict['CoordValida'] = 'N'
        else:  # se la lista non e' valida assumo che le coordinate non sono valide
            datiDict['CoordValida'] = 'N'

        listOfDict.append(datiDict)

    return listOfDict

def validitaLista(lista):
    '''
    metodo per la validazione della lista
	-1 flag set FlagStrNonValida
	-2 flag set FlagRecDuplicato
    @param lista: list
    @return: list
    '''
    listaApp = []
    for ll in lista:
        if len(ll) == 67:
            ll = ll + 'S'  # lista valida
        else:
            i = len(ll)
            for r in range(i, 67):
                ll = ll + 'X'
        listaApp.append(ll)

    # controllo se una lista e' duplicata
    listOfList = []
    C = Counter(listaApp)
    for key, value in C.items():
        if value > 1:
            key = key + 'S'
        else:
            key = key + 'N'
        listOfList.append([key, ] * value)

    ris = [val for sublist in listOfList for val in sublist]  # il check del duplicato ritorna una lista di liste, trasformo in una lista


    return ris

def checkCoord(s):
    '''
    controllo se le coordinate sono nel formato corretto
    @param dicT:
    @return: boolean
    '''
    ris = False
    if len(s) == 9 and string.find(s,',') == 2:
        f = s.split(',')
        if len(f[0]) == 2 and len(f[1]) == 6:
            ris = True
    return ris

