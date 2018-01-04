import peewee
import logging
from ConfigParser import SafeConfigParser
#db = connect(os.environ.get('DATABASE') or 'sqlite:///default.db')
#mysql://user:passwd@ip:port/my_db 


"""
CREATE TABLE test (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(30) NOT NULL,
numero VARCHAR(30) NOT NULL,
reg_date TIMESTAMP
) 
"""
host = ''
user = ''
passwd = ''
port = ''
db = ''

def setParamiter(fileParser = '/home/marco/sviluppo/sopla/test/codice/socket/paramiter.ini'):
    global host,user,passwd,db
    config = SafeConfigParser()
    config.read(fileParser)

    host = config.get('database', 'database_host')
    user = config.get('database', 'database_user')
    passwd = config.get('database', 'database_password')
    db = config.get('database', 'database_name')


#myDB = peewee.MySQLDatabase("testdb", host="localhost",port=3306,user="user",passwd="1234",)
setParamiter()
myDB = peewee.MySQLDatabase(db, host=host,port=3306,user=user,passwd=passwd,)

class MySQLModel(peewee.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB

class TestS(MySQLModel):
    #print "--DB--"
    logging.info('DB START')
    #name = peewee.CharField()
    dataOra = peewee.CharField(64)
    TipoStr = peewee.CharField(1)
    TsDevice = peewee.CharField(13)
    imei = peewee.CharField(15)
    Latitudine = peewee.CharField(9)
    Longitudine = peewee.CharField(10)
    EstOvest = peewee.CharField(1)
    NordSud = peewee.CharField(1)
    velocita = peewee.CharField(5)
    CoordNewOld = peewee.CharField(1)
    CoordValida = peewee.CharField(1)
    CaricaBatteria = peewee.CharField(1)
    Future = peewee.CharField(10)
    TsRicezione = peewee.CharField(13)
    FlagRecDuplicato = peewee.CharField(1)
    FlagStrNonValida = peewee.CharField(1)
    InviatiJons = peewee.CharField(1)
    idUtente = peewee.IntegerField()
    vuoto02 = peewee.CharField(15)
    vuoto03 = peewee.CharField(15)
    vuoto04 = peewee.CharField(15)

if __name__ == "__main__":
    try:
        TestS.create_table()
        print "TestS table create!  "
    except peewee.OperationalError:
        print "TestS table already exists!"

