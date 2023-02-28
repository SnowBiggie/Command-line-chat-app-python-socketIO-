#import modules 
from socket import *
import pickle
import threading 
import random
import datetime

PORT = 3000 # the port the server is running on 
HOST = '127.0.0.1'

#This is the error simulation program, it's a list of 10 element in the range(0,1)
# 1 being success
# 0 being fail 
# you can set the percentage/ratio of fail and succes depending on the 0s and 1s you put in the list 
# current pass rate = 90%
# fail rate = 10%
# meaning 10% of the messages will be lost or inccorect
ErrorWeight = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

# Stores the information about the users that are currently chatting
usersInChat = set()

# Stores all previous messages
historicalMessages = []

#the function will send a message to a client 
def sendToClient(server ,object, client):
    server.sendto(pickle.dumps(object),client)

# function to send all messages to connected users
def sendMessagesToAllUsers(server, object):
    for user in usersInChat:
        sendToClient(server, object, user)

 
# Function will handle user registry 
# address == [IP, PORT]
def userHandler(server):
    encodedObject, address = server.recvfrom(2048)
    usersInChat.add(address)
    object = pickle.loads(encodedObject)
    if object['body']['message'] == "":
        object['body']['message'] = str(address[0]) + ' '+ str(address[1]) + " ~ " + "Authenticating...\nAuthentication success"
        server.sendto(pickle.dumps(object), address)
        #print('send')
    else:
        message = object['body']['message']
        username = str(object['header']['username'])
        time = str(datetime.datetime.time(object['header']['timestamp']))
        object['body']['message'] = username + '//' + str(address[0]) + ' '+ str(address[1]) + ' --- ' + time.split(':')[0] + ':' + time.split(':')[1] + '~' + message
        
        if object['header']['connection'] == 0:
            object['header']['cache'] = historicalMessages
            object['header']['connection'] = 1
        
        #Error Simulation
        choice = random.choices(ErrorWeight) 
        if choice[0] != 0:
            historicalMessages.append(object['body']['message'])
            threading.Thread(target=sendMessagesToAllUsers, args=(server, object, )).start()
        else:
            object['body']['message'] = ""
            object['body']['error'] = "404"
            sendToClient(server, object, address)


def main():
    
    # creating the server using UDP
    server = socket(AF_INET, SOCK_DGRAM)
    i = 0

    try:
        server.bind((HOST, PORT))
        print(f"running the server on, {HOST} and port {PORT}")
    except:
        print(f"unable to run the server, {HOST} and port {PORT}")

    #user Auth
    

    # keep listening to client connection
    while 1:
        threading.Thread(target=userHandler, args=(server, )).start()
       
        
        

if __name__ == '__main__':
    main()