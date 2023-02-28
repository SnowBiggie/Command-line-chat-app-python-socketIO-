from socket import *
import threading
import datetime
import pickle 


HOST = '127.0.0.1'
PORT = 3000

# Dictionary as a message to be exchanged
object = {'header' : {
    'request': 'send',
    'mode': "chat",
    'cache': [],
    "connection": 0,
    'timestamp': datetime.datetime.now(),
    'username': ''
}, 'body' : {
    'message': '',
    "error": ''
}}

#receives messages to the server
def listernFromServer(clientServer):
    while 1:
        decodedObject, address = clientServer.recvfrom(2048)
        object = pickle.loads(decodedObject)
        if object['body']['message'] != '':
            if object['header']['connection'] == 1:
                for message in object['header']['cache']:
                    username = message.split("~")[0]
                    message = message.split("~")[1]
                    print(f"[{username}] {message}")
            #print(object)
            name = str(object['header']['username'])
            username = object['body']['message'].split("~")[0]
            message = object['body']['message'].split("~")[1]
            time = str(datetime.datetime.time(object['header']['timestamp']))
            #print(time)
            print(f"[{username}] {message}")
        elif object['body']['error'] != '':
            print(object['body']['error'])
            print("Packet lost: please resend the message")
        else:
            print('Message is empty')
 
# send messages to the server
def sendToServer(clientServer):
    while 1:
        message = input()
        if message != '':
            object['header']['mode'] = 'chat'
            object['body']['message'] = message
            clientServer.sendto(pickle.dumps(object), (HOST, PORT))
            object['header']['connection'] = -1
        else: 
            print("Empty message")

# Sends messages to the server 

def communicateToServer(server):
    connect = input("type 'server' to connect to a server: ")
    if connect.lower() != "server":
        exit(0)
    
    server.sendto(pickle.dumps(object),(HOST, PORT))   
    encodedObject, address = server.recvfrom(2048)
    newObject = pickle.loads(encodedObject)
    print(newObject['body']['message'])
    threading.Thread(target=listernFromServer, args=(server, )).start()
    sendToServer(server)


#  main function
def main():
    # creating the server 
    name = input('Enter username: ')
    object['header']['username'] = name
    clientServer = socket(AF_INET, SOCK_DGRAM)
    communicateToServer(clientServer)


if __name__ == '__main__':
    main()