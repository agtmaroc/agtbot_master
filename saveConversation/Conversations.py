from datetime import datetime
class Log:
    def __init__(self):
        pass

    def saveConversations(self, userID, usermessage,botmessage,dbConn):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        mydict = {"userID":userID,"User": usermessage, "Bot": botmessage, "Date": str(self.date) + "/" + str(self.current_time)}
        records = dbConn.info_conversation
        records.insert_one(mydict)

        

    def saveInformation(self,userID,email,dbConn):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        mydict = {"userID":userID, "email":email, "Date": str(self.date) + "/" + str(self.current_time)}
        records = dbConn.info_personne
        if(records.find({"userID":userID}).count() == 0):
            records.insert_one(mydict)
        else:
            pass
