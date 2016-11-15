import socket
from thread import *
import time

class MultiplexerServer:
    answerPage = "<!DOCTYPE html><html><body><H1>Thanks for answer</H1></body></html>"
    timeoutPage = "<!DOCTYPE html><html><body><H1>Timeout</H1></body></html>"

    def __init__(self, multiplexerServerPort, quizServerPort, multiplexerServerIP):
        self.clients = {}
        self.multiplexerServerPort = multiplexerServerPort
        self.quizServerPort = quizServerPort
        self.clientSocketForQuizServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocketForQuizServer.connect((multiplexerServerIP, self.quizServerPort))

        self.serverSocketForClients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocketForClients.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocketForClients.bind((multiplexerServerIP, multiplexerServerPort))
        self.serverSocketForClients.listen(500)

    def listenToClient(self, client, addr):
        questionID = ""
        while True:
            try:
                clientMove = client.recv(2048)
            except socket.timeout:
                client.send(MultiplexerServer.timeoutPage)
                self.clients.setdefault(addr[0], {})
                self.clients[addr[0]].setdefault(questionID, [])
                self.clients[addr[0]][questionID] = ["-1", "-1"]
                start_new_thread(self.sendInformationToWebServer, (addr[0], questionID, "-1", "-1"))
                break
            self.answerTime = time.time()

            if clientMove:
                if clientMove[5] == 'Q':
                    questionID = clientMove[14:clientMove.index(".")]
                    start_new_thread(self.sendQuestionToClient,(client, clientMove))
                elif clientMove[5] == 'S':
                    submittedQuestionId, selectedAnswer = self.parseClientAnswer(clientMove)

                    try:
                        if self.clients[addr[0]][submittedQuestionId]:
                            break
                    except:
                        pass

                    self.resultTime = self.answerTime - self.askTime
                    self.clients.setdefault(addr[0], {})
                    self.clients[addr[0]].setdefault(submittedQuestionId, [])
                    self.clients[addr[0]][submittedQuestionId] = [selectedAnswer, self.resultTime]
                    start_new_thread(self.sendInformationToWebServer,
                                     (addr[0], submittedQuestionId, selectedAnswer, str(self.resultTime)))
                    client.send('HTTP/1.1 200 OK\n')
                    client.send('Content-Type: text/html\n')
                    client.send('\n')
                    client.send(MultiplexerServer.answerPage)
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
        clientWish = "question " + clientWish
        self.clientSocketForQuizServer.send(clientWish)
        question = self.clientSocketForQuizServer.recv(2048)
        connectedClient.send('HTTP/1.1 200 OK\n')
        connectedClient.send('Content-Type: text/html\n')
        connectedClient.send('\n')
        connectedClient.send(question)
        self.askTime = time.time()

    def sendInformationToWebServer(self, addr, questionID, selectedAnswer, resultTime):
        information = "information " + addr + " " + questionID + " " + selectedAnswer + " " + resultTime
        self.clientSocketForQuizServer.send(information)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    localhost = s.getsockname()
    s.close()
    print "Multiplexer server wireless LAN adapter Wi-Fi | IPv4 Address: ", localhost[0]

    multiplexerPort = int(raw_input("Please enter multiplexing server port number: "))
    webPort = int(raw_input("Please enter web server port number: "))

    MS = MultiplexerServer(multiplexerPort, webPort, localhost[0])

    while True:
        connectedClient, addr = MS.serverSocketForClients.accept()
        connectedClient.settimeout(30)
        start_new_thread(MS.listenToClient, (connectedClient, addr))
