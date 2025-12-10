import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
import quiz_app
import quiz_app_advanced
import json_creator


class FeatureCard(QFrame):
    """기능 카드 위젯"""
    def __init__(self, title, description, button_text, color, on_click, parent=None):
        super().__init__(parent)
        self.color = color
        self.on_click = on_click
        self.initUI(title, description, button_text)
    
    def initUI(self, title, description, button_text):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 16px;
                border: none;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 28, 24, 24)
        layout.setSpacing(12)
        
        # 색상 원형 인디케이터
        indicator = QLabel()
        indicator.setFixedSize(48, 48)
        indicator.setStyleSheet(f"""
            background-color: {self.color};
            border-radius: 24px;
        """)
        indicator.setAlignment(Qt.AlignCenter)
        
        indicator_container = QHBoxLayout()
        indicator_container.addStretch()
        indicator_container.addWidget(indicator)
        indicator_container.addStretch()
        layout.addLayout(indicator_container)
        
        layout.addSpacing(8)
        
        # 제목
        title_label = QLabel(title)
        title_label.setFont(QFont('Pretendard', 16, QFont.Bold))
        title_label.setStyleSheet('color: #1e293b; background: transparent;')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 설명
        desc_label = QLabel(description)
        desc_label.setFont(QFont('Pretendard', 11))
        desc_label.setStyleSheet('color: #64748b; background: transparent;')
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # 버튼
        button = QPushButton(button_text)
        button.setFont(QFont('Pretendard', 12, QFont.Medium))
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(44)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(self.color)};
            }}
        """)
        button.clicked.connect(self.on_click)
        layout.addWidget(button)
    
    def darken_color(self, hex_color):
        """색상을 약간 어둡게"""
        color_map = {
            '#10b981': '#059669',
            '#6366f1': '#4f46e5',
            '#f59e0b': '#d97706',
        }
        return color_map.get(hex_color, hex_color)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('🎓 Quiz App Launcher')
        self.setGeometry(100, 100, 750, 580)
        self.setMinimumSize(700, 550)
        
        # 전체 배경 스타일
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8fafc, stop:0.3 #f1f5f9, stop:0.7 #e2e8f0, stop:1 #f8fafc);
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Header
        header_label = QLabel('🎓 Quiz App')
        header_label.setFont(QFont('Pretendard', 32, QFont.Bold))
        header_label.setStyleSheet('color: #1e293b; background: transparent;')
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        subtitle = QLabel('학습을 더 재미있게! 원하는 기능을 선택하세요')
        subtitle.setFont(QFont('Pretendard', 13))
        subtitle.setStyleSheet('color: #64748b; background: transparent;')
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(15)

        # 카드 컨테이너
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # Basic Quiz Card
        basic_card = FeatureCard(
            title='Basic Quiz',
            description='정확히 일치하는 답만\n정답으로 인정합니다',
            button_text='시작하기',
            color='#10b981',
            on_click=self.startQuizApp
        )
        cards_layout.addWidget(basic_card)

        # AI Quiz Card
        ai_card = FeatureCard(
            title='AI Quiz',
            description='OpenAI가 답변을 분석하여\n유연하게 채점합니다',
            button_text='시작하기',
            color='#6366f1',
            on_click=self.startAdvancedQuizApp
        )
        cards_layout.addWidget(ai_card)

        # JSON Creator Card
        creator_card = FeatureCard(
            title='JSON Creator',
            description='퀴즈용 JSON 파일을\n쉽게 만들어보세요',
            button_text='만들기',
            color='#f59e0b',
            on_click=self.startJSONCreator
        )
        cards_layout.addWidget(creator_card)

        main_layout.addLayout(cards_layout)
        main_layout.addStretch()

        # Footer
        footer = QLabel('Made with love for better learning')
        footer.setFont(QFont('Pretendard', 10))
        footer.setStyleSheet('color: #94a3b8; background: transparent;')
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

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
    app.setStyle('Fusion')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
