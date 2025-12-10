import json
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QFileDialog, QMessageBox, QFrame,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class ModernButton(QPushButton):
    """모던한 스타일의 버튼"""
    def __init__(self, text, primary=True, danger=False, parent=None):
        super().__init__(text, parent)
        self.primary = primary
        self.danger = danger
        self.setFont(QFont('Pretendard', 12, QFont.Medium))
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(48)
        self.updateStyle()
    
    def updateStyle(self):
        if self.danger:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #fef2f2;
                    color: #dc2626;
                    border: 2px solid #fecaca;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #fee2e2;
                    border-color: #fca5a5;
                }
                QPushButton:pressed {
                    background-color: #fecaca;
                }
            """)
        elif self.primary:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #f59e0b, stop:1 #d97706);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #d97706, stop:1 #b45309);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #b45309, stop:1 #92400e);
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


class ModernTextEdit(QTextEdit):
    """모던한 스타일의 텍스트 에디터"""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setFont(QFont('Pretendard', 13))
        self.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 14px;
                padding: 14px;
                color: #1e293b;
                selection-background-color: #f59e0b;
            }
            QTextEdit:focus {
                border-color: #f59e0b;
                background-color: white;
            }
        """)


class JSONCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('📋 JSON Creator')
        self.setGeometry(100, 100, 700, 650)
        self.setMinimumSize(650, 600)
        
        # 전체 배경 스타일
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #fffbeb, stop:0.5 #fef3c7, stop:1 #fff7ed);
            }
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #1e293b;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #f59e0b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #d97706;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_label = QLabel('📋 JSON Creator')
        header_label.setFont(QFont('Pretendard', 28, QFont.Bold))
        header_label.setStyleSheet('color: #1e293b; background: transparent;')
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        subtitle = QLabel('퀴즈용 JSON 파일을 쉽게 만들어보세요')
        subtitle.setFont(QFont('Pretendard', 12))
        subtitle.setStyleSheet('color: #64748b; background: transparent;')
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(5)

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
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(18)

        # 문제 입력
        question_header = QLabel('📝 문제 입력')
        question_header.setFont(QFont('Pretendard', 13, QFont.Medium))
        question_header.setStyleSheet('color: #475569; background: transparent;')
        card_layout.addWidget(question_header)

        self.question_input = ModernTextEdit('문제를 한 줄에 하나씩 입력하세요')
        self.question_input.setMinimumHeight(120)
        card_layout.addWidget(self.question_input)

        # 정답 입력
        answer_header = QLabel('✅ 정답 입력')
        answer_header.setFont(QFont('Pretendard', 13, QFont.Medium))
        answer_header.setStyleSheet('color: #475569; background: transparent;')
        card_layout.addWidget(answer_header)

        self.answer_input = ModernTextEdit('정답을 문제와 같은 순서로 한 줄에 하나씩 입력하세요')
        self.answer_input.setMinimumHeight(120)
        card_layout.addWidget(self.answer_input)

        # 안내 문구
        hint_label = QLabel('💡 Tip: 문제와 정답의 줄 수가 같아야 합니다')
        hint_label.setFont(QFont('Pretendard', 11))
        hint_label.setStyleSheet('color: #94a3b8; background: transparent;')
        card_layout.addWidget(hint_label)

        card_layout.addSpacing(5)

        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.clear_button = ModernButton('🗑️ 초기화', primary=False, danger=True)
        self.clear_button.clicked.connect(self.clearInputs)
        button_layout.addWidget(self.clear_button)

        self.create_button = ModernButton('💾 JSON 파일 생성', primary=True)
        self.create_button.clicked.connect(self.createJSON)
        button_layout.addWidget(self.create_button, 2)

        card_layout.addLayout(button_layout)

        main_layout.addWidget(card)
        self.setLayout(main_layout)

    def createJSON(self):
        questions = self.question_input.toPlainText().splitlines()
        answers = self.answer_input.toPlainText().splitlines()

        # 빈 줄 제거
        questions = [q.strip() for q in questions if q.strip()]
        answers = [a.strip() for a in answers if a.strip()]

        if len(questions) == len(answers):
            data = {q: a for q, a in zip(questions, answers) if q and a}

            if data:
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getSaveFileName(
                    self, "JSON 파일 저장", "", "JSON Files (*.json)", options=options
                )

                if file_name:
                    if not file_name.endswith('.json'):
                        file_name += '.json'
                    
                    with open(file_name, 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

                    msg = QMessageBox(self)
                    msg.setWindowTitle('성공')
                    msg.setText(f'JSON 파일이 생성되었습니다!\n\n총 {len(data)}개의 문제가 저장되었습니다.')
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                    self.clearInputs()
            else:
                msg = QMessageBox(self)
                msg.setWindowTitle('경고')
                msg.setText('입력된 문제와 정답이 없습니다.')
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle('오류')
            msg.setText(f'문제와 정답의 개수가 일치하지 않습니다.\n\n문제: {len(questions)}개\n정답: {len(answers)}개')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def clearInputs(self):
        self.question_input.clear()
        self.answer_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    json_creator = JSONCreator()
    json_creator.show()
    sys.exit(app.exec_())
