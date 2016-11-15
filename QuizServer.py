import os
import socket

def editQuestions(action, question):
    questionFolder = open(question, "r")
    tmp = questionFolder.read()
    questionFolder.close()
    index = tmp.index("action")

    if tmp[index+8] == "h":
        return

    os.remove(question)
    tmp = tmp[:index+8] + action + tmp[index+8:]
    questionFolder = open(question, "w")
    questionFolder.write(tmp)
    questionFolder.close()

class QuizServer:

    def __init__(self, quizServerPort, localhost):
        self.localhost = localhost
        self.quizServerPort = quizServerPort
        self.quizServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.quizServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.quizServerSocket.bind((self.localhost, quizServerPort))
        self.quizServerSocket.listen(500)

    def getQuestion(self, clientWish):
        questionFolder = open(clientWish, "r")
        question = questionFolder.read()
        questionFolder.close()
        return question

if __name__ == "__main__":
    answers = {'1': "c", '2': "b", '3': "d", '4': "a", '5': "c"}

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    localhost = s.getsockname()
    s.close()
    print "Quiz server wireless LAN adapter Wi-Fi | IPv4 Address: ", localhost[0]

    score = {}
    clients = {}
    clientIP = ""
    submittedQuestionId = ""
    selectedAnswer = ""
    resultTime = ""
    command = ""

    webPort = int(raw_input("Please enter web server port number: "))
    multiplexerPort = int(raw_input("Please enter multiplexer server port number: "))
    tmp = "http://" + localhost[0] + ":" + str(multiplexerPort) + "/SaveAnswer"

    editQuestions(tmp, "Question_1.html")
    editQuestions(tmp, "Question_2.html")
    editQuestions(tmp, "Question_3.html")
    editQuestions(tmp, "Question_4.html")
    editQuestions(tmp, "Question_5.html")
    QS = QuizServer(webPort, localhost[0])

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

            if selectedAnswer == "-1":
                print "client: " + clientIP + " did not answer the " + submittedQuestionId + \
                      ". question." + " Correct answer is " + str(answers[submittedQuestionId]) + ". Client's score: 0"
            else:
                print "client: " + clientIP + "\tQuestion Number: " + submittedQuestionId + \
                      "\tAnswer: " + selectedAnswer + "\tResponse Time: " + resultTime + \
                      "\tClient's score: " + str(score[clientIP][submittedQuestionId]) + \
                      " (Correct answer is " + answers[submittedQuestionId] + ".)"

    multiplexerSocket.close()