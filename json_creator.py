import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox

class JSONCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('JSON Creator')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText('Enter questions (one per line)')
        layout.addWidget(self.question_input)

        self.answer_input = QTextEdit()
        self.answer_input.setPlaceholderText('Enter answers (one per line, in the same order as questions)')
        layout.addWidget(self.answer_input)

        button_layout = QHBoxLayout()

        self.create_button = QPushButton('Create JSON')
        self.create_button.clicked.connect(self.createJSON)
        button_layout.addWidget(self.create_button)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clearInputs)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def createJSON(self):
        questions = self.question_input.toPlainText().splitlines()
        answers = self.answer_input.toPlainText().splitlines()

        if len(questions) == len(answers):
            data = {q: a for q, a in zip(questions, answers) if q and a}

            if data:
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getSaveFileName(self, "Save JSON File", "", "JSON Files (*.json)", options=options)

                if file_name:
                    with open(file_name, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False)

                    QMessageBox.information(self, 'JSON Created', 'JSON 파일이 성공적으로 생성되었습니다.')
                    self.clearInputs()
            else:
                QMessageBox.warning(self, 'Empty Data', '입력된 문제와 정답이 없습니다.')
        else:
            QMessageBox.warning(self, 'Invalid Input', '문제와 정답의 개수가 일치하지 않습니다.')

    def clearInputs(self):
        self.question_input.clear()
        self.answer_input.clear()

if __name__ == '__main__':
    app = QApplication([])
    json_creator = JSONCreator()
    json_creator.show()
    app.exec_()