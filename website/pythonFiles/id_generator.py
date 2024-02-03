# Can call shelve
import shelve

class Generator():
    def __init__(self):
        self.counter = 1
    
    def checkID(self):
        uids = self.readID()
        print(uids)
        # check if it's first instance of db
        if uids:
            # get last id number
            uid = uids[-1]
            print(uid)
            print("old counter =", uid)
            # updates id [not using self.counter cuz old self.counter will always be 1 since it is set]
            uid += 1
            print("new counter =", uid)
            return uid
        else:
            # set first instance of id / set first id
            print("First time @ checkID function")
            uid = self.counter
            return uid
    
    # Check for existing ID in shelve
    def readID(self):
        db = shelve.open("storage.db", "c")
        ids = {}
        try:
            ids = db['Products']
            print("Got Data")
            uids = []

            for key, value in ids.items():
                print(key)
                x = key
                print("At readID function, x=", x)
                uids.append(x)
            return uids
        except:
            print("First time entering id_generator.py")
            pass