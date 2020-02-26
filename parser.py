import datetime
import sys
import pandas as pd
import os

class Message:
    def __init__(self, time, username, line, content, isMedia):
        self.time = time
        self.line = line
        self.username = username
        self.content = content
        self.isMedia = isMedia

    def toDict(self):
        return{
            "time": self.time,
            "username": self.username,
            "content": self.content,
            "isMedia": self.isMedia
        }

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def parseMsg(input):
    line = input.rstrip()
    day = int(line[0:2])
    month = int(line[3:5])
    year = int(line[6:10])
    hour = int(line[12:14])
    minute = int(line[15:17])
    content = line[20:].split(':')[1].rstrip().lstrip()
    content = deEmojify(content)
    if content == '':
        content = "EMOJI"
    user = deEmojify(line[20:].split(':')[0]).rstrip()
    time = datetime.datetime(year, month, day, hour, minute)
    isMedia = False
    if content.find("Media omitted"):
        isMedia = True
    return Message(time, user, line, content, isMedia)


#   read conversation file and create a list with its parsed msgs
def readFromFile(filepath):
    msgList = []
    with open(filepath, encoding="utf-8") as fp:
        line = fp.readline()
        while line:
            if len(line) > 0 and line.find("created group") == -1 and line.find("changed the subject") == -1 and line.find("security code changed") == -1 and line.find("You created group") == -1 and line.find("Messages to this group are now secured with") == -1 and line.find("You changed this group's icon") == -1 and line != "\n" and line.find("Messages to this chat and calls") == -1 and (line[0:2].isnumeric() and line[2] == "/") and line.find("added") == -1 and line.find("removed") == -1 and line.find("left") == -1 and line.find("changed the group description") == -1:
                # parse line to message
                msg = parseMsg(line)
                msgList.append(msg)
            line = fp.readline()
    fp.close()
    return msgList

msgList = readFromFile(sys.argv[1])
df = pd.DataFrame.from_records([msg.toDict() for msg in msgList])
df.to_csv(os.path.splitext(sys.argv[1])[0]+".csv")