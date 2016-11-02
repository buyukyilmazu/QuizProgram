import socket
import threading


class MultiplexerServer:
    localhost = "127.0.0.1"
    subscribers = {}

    def __init__(self, multiplexerServerPort, quizServerPort):
        self.multiplexerServerPort = multiplexerServerPort
        self.quizServerPort = quizServerPort
        self.clientSocketForQuizServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.serverSocketForClients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocketForClients.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocketForClients.bind(('', multiplexerServerPort))
        self.serverSocketForClients.listen(10)

    def listen(self):
        while True:
            connectedClient, addr = self.acceptClients()
            connectedClient.settimeout(10)
            threading.Thread(target=self.listenToClient, args=(connectedClient, addr)).start()
            print "2"


    def acceptClients(self):
        return self.serverSocketForClients.accept()

    def listenToClient(self, client, addr):
        while True:
            clientMove = client.recv(2048)
            if clientMove:
                if clientMove[5] == 'Q':
                    self.giveQuestionToClient(client, clientMove)
                elif clientMove[5] == 'S':
                    questionNumber, answer = self.takeAnswerToClient(clientMove)
                    print questionNumber, answer

    def sendToClient(self, client, message):
        client.send(message)

    def connectToQuizServer(self):
        self.clientSocketForQuizServer.connect((MultiplexerServer.localhost, self.quizServerPort))

    def listenToQuizServer(self):
        return self.clientSocketForQuizServer.recv(2048)

    def sendToQuizServer(self, message):
        self.clientSocketForQuizServer.send(message)

    def parseClientWish(self, clientWish):
        result = clientWish.split("\n")
        index = result[0].index("HTTP")
        return result[0][5:index - 1]

    def parseClientAnswer(self, clientAnswer):
        result = clientAnswer.split("\n")
        index = result[0].index("submitted_question_id")
        index2 = result[0].index("&")
        submittedQuestionId = result[0][index+22:index2]
        index = result[0].index("selected_answer")
        index2 = result[0].index("HTTP")
        selectedAnswer = result[0][index+16:index2 - 1]
        return submittedQuestionId, selectedAnswer

    def sendQuestionToClient(self, connectedClient, question):
        connectedClient.send('HTTP/1.1 200 OK\n')
        connectedClient.send('Content-Type: text/html\n')
        connectedClient.send('\n')
        connectedClient.send(question)

    def giveQuestionToClient(self, connectedClient, clientWish):
        clientWish = self.parseClientWish(clientWish)
        self.connectToQuizServer()
        self.sendToQuizServer(clientWish)
        question = self.listenToQuizServer()
        self.sendQuestionToClient(connectedClient, question)

    def takeAnswerToClient(self, clientAnswer):
        return self.parseClientAnswer(clientAnswer)


if __name__ == "__main__":
    questionNumber = ""
    answer = ""
    MultiplexerServer(13000, 12000).listen()
    # while True:
    #     connectedClient, addr = aa.acceptClients()
    #     threading.Thread(target=aa.listenToClient, args=(connectedClient, addr)).start()
        # print clientMove
        # if clientMove == "":
        #     continue
        # elif clientMove[5] == 'Q':
        #     aa.giveQuestionToClient(connectedClient, clientMove)
        # elif clientMove[5] == 'S':
        #     questionNumber, answer = aa.takeAnswerToClient(clientMove)
        #
        # print addr, questionNumber, answer
