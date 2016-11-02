import socket


class QuizServer:
    localhost = "127.0.0.1"

    def __init__(self, quizServerPort):
        self.quizServerPort = quizServerPort
        self.quizServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.quizServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.quizServerSocket.bind((QuizServer.localhost, quizServerPort))
        self.quizServerSocket.listen(1)

    def acceptToClient(self):
        return self.quizServerSocket.accept()

    def listenToClient(self, multiplexerSocket):
        return multiplexerSocket.recv(2048)

    def sendToClient(self, multiplexerSocket, question):
        multiplexerSocket.send(question)

    def getQuestion(self, clientWish):
        questionFolder = open(clientWish, "r")
        question = questionFolder.read()
        questionFolder.close()
        return question


if __name__ == "__main__":
    aa = QuizServer(12000)
    while True:
        multiplexerSocket, addr = aa.acceptToClient()
        clientWish = aa.listenToClient(multiplexerSocket)
        question = aa.getQuestion(clientWish)
        aa.sendToClient(multiplexerSocket, question)

