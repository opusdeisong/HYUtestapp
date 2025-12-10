import sys
import random
import json
import os
import shutil
from openai import OpenAI
from dotenv import load_dotenv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QStackedWidget, QFileDialog,
    QFrame, QProgressBar, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ModernButton(QPushButton):
    """모던한 스타일의 버튼"""
    def __init__(self, text, primary=True, parent=None):
        super().__init__(text, parent)
        self.primary = primary
        self.setFont(QFont('Pretendard', 12, QFont.Medium))
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(48)
        self.updateStyle()
    
    def updateStyle(self):
        if self.primary:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6366f1, stop:1 #8b5cf6);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4f46e5, stop:1 #7c3aed);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4338ca, stop:1 #6d28d9);
                }
                QPushButton:disabled {
                    background: #94a3b8;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f1f5f9;
                    color: #475569;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #e2e8f0;
                    border-color: #cbd5e1;
                }
                QPushButton:pressed {
                    background-color: #cbd5e1;
                }
            """)


class ModernLineEdit(QLineEdit):
    """모던한 스타일의 입력 필드"""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setFont(QFont('Pretendard', 14))
        self.setMinimumHeight(56)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 14px;
                padding: 14px 20px;
                color: #1e293b;
                selection-background-color: #6366f1;
            }
            QLineEdit:focus {
                border-color: #6366f1;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
        """)


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.Ques = {}
        self.total_questions = 0
        self.current_question_index = 0
        self.correct_count = 0
        self.json_file = ""
        self.json_file_copy = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle('🤖 AI Quiz App')
        self.setGeometry(100, 100, 650, 550)
        self.setMinimumSize(600, 500)
        
        # 전체 배경 스타일
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f0f4ff, stop:0.5 #faf5ff, stop:1 #fff7ed);
            }
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #1e293b;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4f46e5;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_label = QLabel('🤖 AI Quiz App')
        header_label.setFont(QFont('Pretendard', 28, QFont.Bold))
        header_label.setStyleSheet('color: #1e293b; background: transparent;')
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        subtitle = QLabel('AI가 채점하는 스마트 퀴즈 시스템')
        subtitle.setFont(QFont('Pretendard', 12))
        subtitle.setStyleSheet('color: #64748b; background: transparent;')
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(10)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet('background: transparent;')
        main_layout.addWidget(self.stack)

        # Welcome Page
        self.welcome_page = self.createWelcomePage()
        self.stack.addWidget(self.welcome_page)

        # Quiz Page
        self.quiz_page = QuizPage(self)
        self.stack.addWidget(self.quiz_page)

        self.setLayout(main_layout)

    def createWelcomePage(self):
        page = QFrame()
        page.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: none;
            }
        """)
        
        # 그림자 효과
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 25))
        page.setGraphicsEffect(shadow)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 50, 40, 50)
        layout.setSpacing(25)

        # 색상 원형 인디케이터
        indicator = QLabel()
        indicator.setFixedSize(64, 64)
        indicator.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #6366f1, stop:1 #8b5cf6);
            border-radius: 32px;
        """)
        
        indicator_container = QHBoxLayout()
        indicator_container.addStretch()
        indicator_container.addWidget(indicator)
        indicator_container.addStretch()
        layout.addLayout(indicator_container)

        guide_label = QLabel('퀴즈를 시작하려면\nJSON 파일을 선택하세요')
        guide_label.setFont(QFont('Pretendard', 16))
        guide_label.setStyleSheet('color: #475569; background: transparent;')
        guide_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(guide_label)

        layout.addSpacing(20)

        # 파일 선택 버튼
        self.select_button = ModernButton('📁 JSON 파일 선택', primary=True)
        self.select_button.clicked.connect(self.selectJSONFile)
        layout.addWidget(self.select_button)

        # 안내 텍스트
        hint_label = QLabel('💡 Tip: 문제와 정답이 담긴 JSON 파일을 준비하세요')
        hint_label.setFont(QFont('Pretendard', 11))
        hint_label.setStyleSheet('color: #94a3b8; background: transparent;')
        hint_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint_label)

        layout.addStretch()
        return page

    def selectJSONFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "JSON 파일 선택", "", "JSON Files (*.json)", options=options
        )
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
                self.Ques = json.load(file)
                self.total_questions = len(self.Ques)
                return self.Ques
        except FileNotFoundError:
            return {}

    def saveQuestions(self):
        with open(self.json_file_copy, 'w', encoding='utf-8') as file:
            json.dump(self.Ques, file, ensure_ascii=False)

    def nextQuestion(self):
        if len(self.Ques) == 0:
            accuracy = (self.correct_count / self.total_questions) * 100 if self.total_questions > 0 else 0
            self.showCompletionDialog(accuracy)
        else:
            self.question = random.choice(list(self.Ques.keys()))
            self.current_question_index += 1
            self.quiz_page.updateQuestion(self.question)
            self.quiz_page.answer_input.clear()
            self.quiz_page.answer_input.setFocus()
            self.updateProgressLabel()

    def showCompletionDialog(self, accuracy):
        msg = QMessageBox(self)
        msg.setWindowTitle('퀴즈 완료!')
        
        if accuracy >= 90:
            grade = '최고예요!'
        elif accuracy >= 70:
            grade = '잘했어요!'
        elif accuracy >= 50:
            grade = '괜찮아요!'
        else:
            grade = '더 공부해봐요!'
        
        msg.setText(f'{grade}\n\n정답률: {accuracy:.1f}%\n맞은 문제: {self.correct_count}/{self.total_questions}')
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        self.close()

    def checkAnswer(self):
        user_answer = self.quiz_page.answer_input.text().strip()
        if not user_answer:
            return
        
        # 버튼 비활성화 (중복 클릭 방지)
        self.quiz_page.submit_button.setEnabled(False)
        self.quiz_page.submit_button.setText('AI가 채점 중...')
        QApplication.processEvents()
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                temperature=0,
                max_tokens=10,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a quiz judge. Compare the user's answer to the correct answer. Reply with ONLY 'Yes' if correct (even if phrased differently or in another language), or 'No' if incorrect."
                    },
                    {
                        "role": "user",
                        "content": f"Question: {self.question}\nCorrect Answer: {self.Ques[self.question]}\nUser's Answer: {user_answer}"
                    }
                ]
            )
            judge_result = response.choices[0].message.content.strip().lower()
        except Exception as e:
            QMessageBox.critical(self, '오류', f'API 호출 중 오류가 발생했습니다:\n{str(e)}')
            self.quiz_page.submit_button.setEnabled(True)
            self.quiz_page.submit_button.setText('제출하기')
            return
        
        # 버튼 복구
        self.quiz_page.submit_button.setEnabled(True)
        self.quiz_page.submit_button.setText('제출하기')
        
        correct_answer = self.Ques[self.question]
        
        if judge_result == "yes":
            self.showResultDialog(True, correct_answer)
            self.correct_count += 1
            self.Ques.pop(self.question)
            self.saveQuestions()
            self.nextQuestion()
        else:
            self.showResultDialog(False, correct_answer)
            self.current_question_index -= 1
            self.saveQuestions()
            self.nextQuestion()

    def showResultDialog(self, is_correct, correct_answer):
        msg = QMessageBox(self)
        if is_correct:
            msg.setWindowTitle('정답!')
            msg.setText(f'정답입니다!\n\n정답: {correct_answer}')
            msg.setIcon(QMessageBox.Information)
        else:
            msg.setWindowTitle('오답')
            msg.setText(f'틀렸습니다.\n\n정답: {correct_answer}')
            msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def showQuizPage(self):
        self.stack.setCurrentWidget(self.quiz_page)
        self.quiz_page.resetStats(self.total_questions)
        self.nextQuestion()

    def updateProgressLabel(self):
        remaining = len(self.Ques)
        solved = self.total_questions - remaining
        self.quiz_page.updateProgress(solved, self.total_questions, self.correct_count)

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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # 카드 컨테이너
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: none;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 25))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 30, 35, 30)
        card_layout.setSpacing(20)

        # 상단 진행 상태 바
        progress_container = QFrame()
        progress_container.setStyleSheet('background: transparent;')
        progress_layout = QHBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)

        self.progress_label = QLabel('진행: 0/0')
        self.progress_label.setFont(QFont('Pretendard', 11, QFont.Medium))
        self.progress_label.setStyleSheet('color: #6366f1; background: transparent;')
        progress_layout.addWidget(self.progress_label)

        progress_layout.addStretch()

        self.score_label = QLabel('정답: 0개')
        self.score_label.setFont(QFont('Pretendard', 11, QFont.Medium))
        self.score_label.setStyleSheet('color: #10b981; background: transparent;')
        progress_layout.addWidget(self.score_label)

        card_layout.addWidget(progress_container)

        # 진행률 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximumHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #e2e8f0;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6);
                border-radius: 4px;
            }
        """)
        card_layout.addWidget(self.progress_bar)

        card_layout.addSpacing(10)

        # 문제 라벨
        question_header = QLabel('📝 문제')
        question_header.setFont(QFont('Pretendard', 12, QFont.Medium))
        question_header.setStyleSheet('color: #64748b; background: transparent;')
        card_layout.addWidget(question_header)

        self.question_label = QLabel()
        self.question_label.setFont(QFont('Pretendard', 16, QFont.Medium))
        self.question_label.setStyleSheet("""
            color: #1e293b;
            background-color: #f8fafc;
            border: none;
            border-radius: 12px;
            padding: 20px;
        """)
        self.question_label.setWordWrap(True)
        self.question_label.setMinimumHeight(100)
        self.question_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        card_layout.addWidget(self.question_label)

        card_layout.addSpacing(5)

        # 답변 입력
        answer_header = QLabel('✏️ 정답 입력')
        answer_header.setFont(QFont('Pretendard', 12, QFont.Medium))
        answer_header.setStyleSheet('color: #64748b; background: transparent;')
        card_layout.addWidget(answer_header)

        self.answer_input = ModernLineEdit('정답을 입력하세요...')
        self.answer_input.returnPressed.connect(self.parent.checkAnswer)
        card_layout.addWidget(self.answer_input)

        card_layout.addSpacing(10)

        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.skip_button = ModernButton('건너뛰기', primary=False)
        self.skip_button.clicked.connect(self.skipQuestion)
        button_layout.addWidget(self.skip_button)

        self.submit_button = ModernButton('제출하기', primary=True)
        self.submit_button.clicked.connect(self.parent.checkAnswer)
        button_layout.addWidget(self.submit_button, 2)

        card_layout.addLayout(button_layout)

        layout.addWidget(card)
        self.setLayout(layout)

    def updateQuestion(self, question):
        self.question_label.setText(question)

    def updateProgress(self, solved, total, correct):
        self.progress_label.setText(f'진행: {solved}/{total}')
        self.score_label.setText(f'정답: {correct}개')
        if total > 0:
            self.progress_bar.setValue(int((solved / total) * 100))

    def resetStats(self, total):
        self.progress_bar.setValue(0)
        self.progress_label.setText(f'진행: 0/{total}')
        self.score_label.setText('정답: 0개')

    def skipQuestion(self):
        self.parent.current_question_index -= 1
        self.parent.nextQuestion()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 시스템 폰트 설정
    app.setStyle('Fusion')
    
    quiz_app = QuizApp()
    quiz_app.show()
    sys.exit(app.exec_())
