# Python file to control I/O - reading and writing to chat logs
from datetime import date

from ServerBackend import UserList
from ServerBackend import Messages

f = open("ChatRecord" + str(date.today()), "a")

f.write("Users:")

for i in UserList:
    f.write(str(i) + ", ")

for x in Messages:
    f.write(str(x)+ "\n")





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