import socket
import uuid

localhost = "127.0.0.1"
quizServerPort = 12000
multiplexerClient = None

clients = []
clientGrades = {}

questions = {
    1 : 'Question_1.html',
    2 : 'Question_2.html',
    3 : 'Question_3.html',
}

quizStarted = False

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((localhost, quizServerPort))
serverSocket.listen(1)

def startQuiz(data):
    return

def addNewPlayer(id):

    clients.append(id)
    multiplexerClient.send(getQuestion(1, id))
    print clients

def updateGrades(data):
    return

def getQuestion(questionIndex, id):
    questionFolder = open(questions[questionIndex], "r")
    questionHtml = questionFolder.read()
    questionFolder.close()

    questionHtml = questionHtml.replace("name='client_id' value='null'", "name='client_id' value='"+id+"'");

    return questionHtml

if __name__ == "__main__":

    multiplexerClient, addr = serverSocket.accept()

    while True:

        message = multiplexerClient.recv(1024)
        if(len(message) > 1):
            message = message.split('&')
            mType = int(message[0])
            if(mType == 0):
                startQuiz(message[1])
            elif(mType == 1):
                addNewPlayer(message[1])
            elif(mType == 2):
                updateGrades(message[1])
            elif(mType == 3):
                multiplexerClient.send(getQuestion(2,message[1]))

    multiplexerClient.close()
