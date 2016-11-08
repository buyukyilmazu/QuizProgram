import socket
from thread import *
import time

class MultiplexerServer:
    localhost = "127.0.0.1"
    answerPage = "<!DOCTYPE html><html><body><H1>Thanks for answer</H1></body></html>"
    timeoutPage = "<!DOCTYPE html><html><body><H1>Timeout</H1></body></html>"

    def __init__(self, multiplexerServerPort, quizServerPort):
        self.clients = {}
        self.questionID = ""
        self.nextQuestion = False
        self.multiplexerServerPort = multiplexerServerPort
        self.quizServerPort = quizServerPort
        self.clientSocketForQuizServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocketForQuizServer.connect((MultiplexerServer.localhost, self.quizServerPort))

        self.serverSocketForClients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocketForClients.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocketForClients.bind(('', multiplexerServerPort))
        self.serverSocketForClients.listen(10)

    def listenToClient(self, client, addr):

        while True:
            try:
                clientMove = client.recv(2048)
            except socket.timeout:
                client.send(MultiplexerServer.timeoutPage)
                self.clients.setdefault(addr[0], []).append([self.questionID, "-1", "-1"])
                break
            self.answerTime = time.time()

            if clientMove:
                if clientMove[5] == 'Q':
                    self.questionID = clientMove[14:clientMove.index(".")]
                    self.sendQuestionToClient(client, clientMove)
                elif clientMove[5] == 'S':
                    submittedQuestionId, selectedAnswer = self.parseClientAnswer(clientMove)

                    if self.clients.get(addr[0]):
                        for i in self.clients[addr[0]]:
                            if i[0] == submittedQuestionId:
                                client.close()
                                return

                    self.resultTime = self.answerTime - self.askTime
                    self.clients.setdefault(addr[0], []).append([submittedQuestionId, selectedAnswer, self.resultTime])
                    client.send('HTTP/1.1 200 OK\n')
                    client.send('Content-Type: text/html\n')
                    client.send('\n')
                    client.send(MultiplexerServer.answerPage)
                    print self.clients
                    break
                else:
                    break
            else:
                break

        client.close()

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
        self.askTime = time.time()

if __name__ == "__main__":
    aa = MultiplexerServer(13000, 12000)

    while True:
        connectedClient, addr = aa.serverSocketForClients.accept()
        connectedClient.settimeout(30)
        start_new_thread(aa.listenToClient, (connectedClient, addr))





















