# Python file to control I/O - reading and writing to chat logs
from datetime import date

from ServerBackend import ServerBackend

filename = f"Record_{date.today()}.txt"
with open(filename, "w") as f:
    f.write("Users:\n")
    f.write(", ".join(ServerBackend.UserList) + "\n")
    f.write("Messages:\n")
    f.writelines(message + "\n" for message in ServerBackend.Messages)

#f = open("ChatRecord" + str(date.today()), "a")

#f.write("Users:")

#for i in ServerBackend.UserList:
 #   f.write(str(i) + ", ")

#for x in ServerBackend.Messages:
 #   f.write(str(x)+ "\n")





"""
class FileManager():
    def __init__():
        # not sure if we need a constructor for this one or not
        return

def loadPreviousChats():
    return

def saveCurrentChat():
    return

"""