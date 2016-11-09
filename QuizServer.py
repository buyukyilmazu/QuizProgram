import socket


class QuizServer:
    localhost = "127.0.0.1"

    def __init__(self, quizServerPort):
        self.quizServerPort = quizServerPort
        self.quizServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.quizServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.quizServerSocket.bind((QuizServer.localhost, quizServerPort))
        self.quizServerSocket.listen(500)

    def getQuestion(self, clientWish):
        questionFolder = open(clientWish, "r")
        question = questionFolder.read()
        questionFolder.close()
        return question

if __name__ == "__main__":
    answers = {'1': "c", '2': "b", '3': "d", '4': "a", '5': "c",
               '6': "a", '7': "d", '8': "b", '9': "e", '10': "e"}
    score = {}
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
        command = command.split()
        if command[0] == "question":
            question = QS.getQuestion(command[1])
            multiplexerSocket.send(question)
            command = ""
        elif command[0] == "information":
            clientIP = command[1]
            submittedQuestionId = command[2]
            selectedAnswer = command[3]
            resultTime = command[4]
            clients.setdefault(clientIP, {})
            clients[clientIP].setdefault(submittedQuestionId, [])
            clients[clientIP][submittedQuestionId] = [selectedAnswer, resultTime]
            if clients[clientIP][submittedQuestionId][0] == answers[submittedQuestionId]:
                questionScore = 10
            else:
                questionScore = 0
            score.setdefault(clientIP, {})
            score[clientIP][submittedQuestionId] = questionScore
            command = ""

    multiplexerSocket.close()
