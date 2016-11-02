import socket
from thread import *


class MultiplexerServer:
    localhost = "127.0.0.1"
    subscribers = {}

    def __init__(self, multiplexerServerPort, quizServerPort):
        self.multiplexerServerPort = multiplexerServerPort
        self.quizServerPort = quizServerPort
        self.clientSocketForQuizServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocketForQuizServer.connect((MultiplexerServer.localhost, self.quizServerPort))

        self.serverSocketForClients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocketForClients.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocketForClients.bind(('', multiplexerServerPort))
        self.serverSocketForClients.listen(10)

    def listenToClient(self, client):
        while True:
            clientMove = client.recv(2048)
            if clientMove == '':
                continue
            elif clientMove[5] == 'Q':
                self.sendQuestionToClient(client, clientMove)
            elif clientMove[5] == 'S':
                self.parseClientAnswer(clientMove)

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

    def sendQuestionToClient(self, connectedClient, clientWish):
        clientWish = self.parseClientWish(clientWish)
        self.clientSocketForQuizServer.send(clientWish)
        question = self.clientSocketForQuizServer.recv(2048)
        connectedClient.send('HTTP/1.1 200 OK\n')
        connectedClient.send('Content-Type: text/html\n')
        connectedClient.send('\n')
        connectedClient.send(question)

if __name__ == "__main__":
    aa = MultiplexerServer(13000, 12000)

    while True:
        connectedClient, addr = aa.serverSocketForClients.accept()
        start_new_thread(aa.listenToClient, (connectedClient,))
