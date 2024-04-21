import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
import quiz_app
import quiz_app_advanced
import json_creator

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quiz App Launcher')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.quiz_button = QPushButton('Start Quiz App')
        self.quiz_button.clicked.connect(self.startQuizApp)
        layout.addWidget(self.quiz_button)

        self.advanced_quiz_button = QPushButton('Start Advanced Quiz App')
        self.advanced_quiz_button.clicked.connect(self.startAdvancedQuizApp)
        layout.addWidget(self.advanced_quiz_button)

        self.creator_button = QPushButton('Start JSON Creator')
        self.creator_button.clicked.connect(self.startJSONCreator)
        layout.addWidget(self.creator_button)

        self.setLayout(layout)

    def startQuizApp(self):
        self.quiz_app = quiz_app.QuizApp()
        self.quiz_app.show()

    def startAdvancedQuizApp(self):
        self.advanced_quiz_app = quiz_app_advanced.QuizApp()
        self.advanced_quiz_app.show()

    def startJSONCreator(self):
        self.json_creator = json_creator.JSONCreator()
        self.json_creator.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())