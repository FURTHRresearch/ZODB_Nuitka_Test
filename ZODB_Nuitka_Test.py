import datetime

from ZODB import DB, FileStorage
fileName = "zodb.db"
dbFile = FileStorage.FileStorage(fileName)
db = DB(dbFile)
from BTrees.OOBTree import OOBTree
import transaction

connection = db.open()
rootObject = connection.root

try:
    storage = rootObject.storage
except:
    rootObject.storage = OOBTree()
    storage = rootObject.storage

try:
    print(storage["a"])
except:
    pass

dateTime = datetime.datetime.now()

rootObject.storage["a"] = dateTime

transaction.commit()



