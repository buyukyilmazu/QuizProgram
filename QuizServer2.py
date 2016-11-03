import socket

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

def addNewPlayer():
    multiplexerClient.send(getQuestion(1))

def updateGrades(data):
    return

def getQuestion(questionIndex):
    questionFolder = open(questions[questionIndex], "r")
    questionHtml = questionFolder.read()
    questionFolder.close()
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
                addNewPlayer()
            elif(mType == 2):
                updateGrades(message[1])
            elif(mType == 3):
                multiplexerClient.send(getQuestion(2))

    multiplexerClient.close()
