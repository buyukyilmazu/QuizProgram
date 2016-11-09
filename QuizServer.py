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
    clients = {}
    clientIP = ""
    submittedQuestionId = ""
    selectedAnswer = ""
    resultTime = ""
    command = ""
    webPort = int(raw_input("Please enter web server port number: "))
    QS = QuizServer(webPort)

    multiplexerSocket, addr = QS.quizServerSocket.accept()

    while True:
        command = multiplexerSocket.recv(2048)
        if command == "sendQuestion":
            clientWish = multiplexerSocket.recv(2048)
            question = QS.getQuestion(clientWish)
            multiplexerSocket.send(question)
            command = ""
        elif command == "getInformation":
            clientIP = multiplexerSocket.recv(2048)
            submittedQuestionId = multiplexerSocket.recv(2048)
            selectedAnswer = multiplexerSocket.recv(2048)
            resultTime = multiplexerSocket.recv(2048)
            clients.setdefault(clientIP, []).append([submittedQuestionId, selectedAnswer, resultTime])
            command = ""
            print clients

    multiplexerSocket.close()
