import sys, anthropic, os, random, json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget, QTextEdit
from dotenv import load_dotenv

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="your api key",
)
class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.Ques = self.loadQuestions()
        self.i = 0
        self.all = len(self.Ques)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quiz App')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.quiz_page = QuizPage(self)
        self.stack.addWidget(self.quiz_page)

        self.add_page = AddQuestionPage(self)
        self.stack.addWidget(self.add_page)

        self.add_button = QPushButton('Add Question')
        self.add_button.clicked.connect(self.showAddPage)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.nextQuestion()

    def nextQuestion(self):
        if len(self.Ques) == 0:
            QMessageBox.information(self, 'Quiz Completed', f'모든 문제를 풀었습니다.\\n정답률: {(self.all / self.i) * 100:.2f}%')
            self.close()
        else:
            self.question = random.choice(list(self.Ques.keys()))
            self.i += 1
            self.quiz_page.question_label.setText(f'Q: {self.question}')
            self.quiz_page.answer_input.clear()

    def checkAnswer(self):
        user_answer = self.quiz_page.answer_input.text()
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0,
            system="From now on, if the question given as a judge and the correct answer are given, you can judge whether the user's answer is correct. At this time, the answer is yes or no",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Q:한국의 수도는? Answer: 서울 User Response: Seoul"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "Yes"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Q:소비자와 소비자의 파트너가 클라우드 서비스를 이용하여 모바일 기기로 클라우드 컴퓨팅 인프라를 구성하여 여러 가지 정보와 자우너을 공유하는 ICT 기술 Answer: 모바일 클라우드 컴퓨팅 User Response: TCP/IP"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "No"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Q:{self.question} Answer: {self.Ques[self.question]} User Response: {user_answer}",
                        }
                    ]
                }
            ]
        )
        judge_result = message.content[0].text


        if judge_result.lower() == "yes":
            QMessageBox.information(self, 'Correct', '정답입니다!')
            self.Ques.pop(self.question)
            self.saveQuestions()
            self.nextQuestion()
        else:
            QMessageBox.warning(self, 'Incorrect', f'틀렸습니다. 정답은 "{self.Ques[self.question]}"입니다.')

    def addQuestion(self, question, answer):
        if question and answer:
            self.Ques[question] = answer
            self.saveQuestions()
            QMessageBox.information(self, 'Question Added', '새로운 문제가 추가되었습니다.')
        else:
            QMessageBox.warning(self, 'Invalid Input', '문제와 정답을 모두 입력해주세요.')

    def showAddPage(self):
        self.stack.setCurrentWidget(self.add_page)

    def showQuizPage(self):
        self.stack.setCurrentWidget(self.quiz_page)
        self.nextQuestion()

    def loadQuestions(self):
        try:
            with open('questions.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def saveQuestions(self):
        with open('questions.json', 'w', encoding='utf-8') as file:
            json.dump(self.Ques, file, ensure_ascii=False)

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

class AddQuestionPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText('Enter new questions (one per line)')
        layout.addWidget(self.question_input)

        self.answer_input = QTextEdit()
        self.answer_input.setPlaceholderText('Enter answers (one per line, in the same order as questions)')
        layout.addWidget(self.answer_input)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.addQuestions)
        button_layout.addWidget(self.add_button)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.parent.showQuizPage)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)


    def addQuestions(self):
        questions = self.question_input.toPlainText().splitlines()
        answers = self.answer_input.toPlainText().splitlines()

        if len(questions) == len(answers):
            for question, answer in zip(questions, answers):
                if question and answer:
                    self.parent.Ques[question] = answer
            self.parent.saveQuestions()
            QMessageBox.information(self, 'Questions Added', f'{len(questions)} 문제가 추가되었습니다.')
            self.question_input.clear()
            self.answer_input.clear()
        else:
            QMessageBox.warning(self, 'Invalid Input', '문제와 정답의 개수가 일치하지 않습니다.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    quiz_app.show()
    sys.exit(app.exec_())