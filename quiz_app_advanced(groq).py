import sys, anthropic
import random
import json
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget, QTextEdit, QFileDialog
from groq import Groq

client = Groq(
    api_key='YOUR_API_KEY',
)
class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.Ques = {}
        self.i = 0
        self.all = len(self.Ques)
        self.json_file = ""
        self.json_file_copy = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quiz App')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.quiz_page = QuizPage(self)
        self.stack.addWidget(self.quiz_page)

        self.select_button = QPushButton('Select JSON File')
        self.select_button.clicked.connect(self.selectJSONFile)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def selectJSONFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)", options=options)
        if file_name:
            self.json_file = file_name
            self.createJSONFileCopy()
            self.Ques = self.loadQuestions()
            self.all = len(self.Ques)
            self.i = 0
            self.showQuizPage()

    def createJSONFileCopy(self):
        base_name = os.path.basename(self.json_file)
        self.json_file_copy = f"copy_{base_name}"
        shutil.copyfile(self.json_file, self.json_file_copy)

    def loadQuestions(self):
        try:
            with open(self.json_file_copy, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def saveQuestions(self):
        with open(self.json_file_copy, 'w', encoding='utf-8') as file:
            json.dump(self.Ques, file, ensure_ascii=False)

    def nextQuestion(self):
        if len(self.Ques) == 0:
            QMessageBox.information(self, 'Quiz Completed', f'모든 문제를 풀었습니다.\n정답률: {(self.all / self.i) * 100:.2f}%')
            self.close()
        else:
            self.question = random.choice(list(self.Ques.keys()))
            self.i += 1
            self.quiz_page.question_label.setText(f'Q: {self.question}')
            self.quiz_page.answer_input.clear()

    def checkAnswer(self):
        user_answer = self.quiz_page.answer_input.text()
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "From now on, if the question given as a judge and the correct answer are given, you can judge whether the user's answer is correct. At this time, the answer is yes or no"
                },
                {
                    "role": "user",
                    "content": "Q:한국의 수도는? Answer: 서울 User Response: Seoul"
                },
                {
                    "role": "assistant",
                    "content": "Yes"
                },
                {
                    "role": "user",
                    "content": "Q:소비자와 소비자의 파트너가 클라우드 서비스를 이용하여 모바일 기기로 클라우드 컴퓨팅 인프라를 구성하여 여러 가지 정보와 자우너을 공유하는 ICT 기술 Answer: 모바일 클라우드 컴퓨팅 User Response: TCP/IP"
                },
                {
                    "role": "assistant",
                    "content": "No"
                },
                {
                    "role": "user",
                    "content": f"Q:{self.question} Answer: {self.Ques[self.question]} User Response: {user_answer}"
                }
            ],
            temperature=0,
            max_tokens=1300,
            top_p=1,
            stream=False,
            stop=None,
        )
        judge_result = completion.choices[0].message.content

        if judge_result.lower() == "yes":
            QMessageBox.information(self, 'Correct', '정답입니다!')
            self.Ques.pop(self.question)
            self.saveQuestions()
            self.nextQuestion()
        else:
            QMessageBox.warning(self, 'Incorrect', f'틀렸습니다. 정답은 "{self.Ques[self.question]}"입니다.')
            self.saveQuestions()
            self.nextQuestion()

    def showQuizPage(self):
        self.stack.setCurrentWidget(self.quiz_page)
        self.nextQuestion()

    def closeEvent(self, event):
        self.deleteJSONFileCopy()
        event.accept()

    def deleteJSONFileCopy(self):
        if self.json_file_copy and os.path.exists(self.json_file_copy):
            os.remove(self.json_file_copy)



class QuizPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.question_label = QLabel()
        layout.addWidget(self.question_label)

        self.answer_input = QLineEdit()
        self.answer_input.returnPressed.connect(self.parent.checkAnswer)  # 엔터 키 이벤트 연결
        layout.addWidget(self.answer_input)

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.parent.checkAnswer)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    quiz_app.show()
    sys.exit(app.exec_())