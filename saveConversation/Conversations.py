from datetime import datetime
class Log:
    def __init__(self):
        pass

    def saveConversations(self, userID, usermessage,botmessage,dbConn):

        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        #db = dbConn['Covid-19DB']  # connecting to the database called crawlerD
        mydict = {"userID":userID,"User": usermessage, "Bot": botmessage, "Date": str(self.date) + "/" + str(self.current_time)}

        #table = db[sessionID]
        records = dbConn.B
        records.insert_one(mydict)

        #table.insert_one(mydict)

    def saveInformation(self,userID,nom,prenom,email,dbConn):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        mydict = {"userID":userID, "nom":nom, "prenom":prenom, "email":email, "Date": str(self.date) + "/" + str(self.current_time)}
        records = dbConn.A
        if(records.find({"userID":userID}).count() == 0):
            records.insert_one(mydict)
        else:
            pass
