import socket
import threading
import uuid
import json

localhost = '127.0.0.1'
multiplexerServerPort = 13000
quizServerPort = 12000

clientCollection = []

quizServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
quizServerSocket.connect((localhost, quizServerPort))

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('', multiplexerServerPort))
serverSocket.listen(10)

messageType = {
    0 : 'createId',
    1 : 'saveAnswer',
    2 : 'startQuiz',
}

def createId():
    return str(uuid.uuid4())

def saveAnswer(data):
    return

def startQuiz():
    return

def normalizeMessage(message):
    if(len(message) > 0):
        return message.split(' ')[1][1:]

    return ''

def getParameters(message):
    parameters = message.split('?')
    if(len(parameters) > 1):
        return parameters[1].split('&')

def getParameter(parameters, name):
    for par in parameters:
        paramater = par.split('=')
        if(paramater[0] == name):
            return paramater[1]

    return ''

def counterTest():
    for client in clientCollection:
        quizServerSocket.send('3&')
        ip, port = client

        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tempSocket.connect((ip, port))

        message = quizServerSocket.recv(4096)

        tempSocket.send('HTTP/1.1 200 OK\n')
        tempSocket.send('Content-Type: text/html\n')
        tempSocket.send('\n')
        tempSocket.send(message)
        tempSocket.close()

def listenToClient(client, clientAddress):
    while True:
        try:
            message = normalizeMessage(client.recv(1024))

            if(message != ''):
                if(message == 'Question_1.html'):

                    clientCollection.append(clientAddress)

                    quizServerSocket.send('1&')

                    message = quizServerSocket.recv(4096)

                    client.send('HTTP/1.1 200 OK\n')
                    client.send('Content-Type: text/html\n')
                    client.send('\n')
                    client.send(message)
                    client.close()
                    return False

                elif(message == '127.0.0.1:13000/GetId'):

                    id = createId()
                    client.send(id)
                    client.close()
                    return False

                elif(message[0] == 'S'):

                    quizServerSocket.send('3&')

                    message = quizServerSocket.recv(4096)

                    client.send('HTTP/1.1 200 OK\n')
                    client.send('Content-Type: text/html\n')
                    client.send('\n')
                    client.send(message)
                    client.close()

                    return False

            print message
        except Exception as e:
            print e
            client.close()
            return False

if __name__ == "__main__":

    while True:
        newClient, clientAddress = serverSocket.accept()
        threading.Thread(target = listenToClient, args = (newClient, clientAddress)).start()
        #threading.Timer(10.0, counterTest).start()
