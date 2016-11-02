import socket


class QuizServer:
    localhost = "127.0.0.1"

    def __init__(self, quizServerPort):
        self.quizServerPort = quizServerPort
        self.quizServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.quizServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.quizServerSocket.bind((QuizServer.localhost, quizServerPort))
        self.quizServerSocket.listen(1)

    def getQuestion(self, clientWish):
        questionFolder = open(clientWish, "r")
        question = questionFolder.read()
        questionFolder.close()
        return question

if __name__ == "__main__":
    aa = QuizServer(12000)
    multiplexerSocket, addr = aa.quizServerSocket.accept()

    while True:
        clientWish = multiplexerSocket.recv(2048)
        question = aa.getQuestion(clientWish)
        multiplexerSocket.send(question)

    multiplexerSocket.close()
