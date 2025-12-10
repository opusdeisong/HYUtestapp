# 🎓 Quiz App

AI가 채점하는 스마트 퀴즈 애플리케이션입니다. Python과 PyQt5로 개발되었으며, OpenAI API를 활용하여 유연한 정답 판단이 가능합니다.

## ✨ 주요 기능

### 📖 Basic Quiz
- JSON 파일에서 문제를 로드하여 퀴즈 진행
- **정확히 일치하는 답만 정답으로 인정**
- 랜덤 문제 출제
- 진행률 및 정답률 표시

### 🤖 AI Quiz
- OpenAI GPT-4.1-mini를 활용한 **스마트 채점**
- 의미적으로 동일한 답변도 정답으로 인정
- 예: "베이징" = "북경" = "Beijing" 모두 정답 처리

### 📋 JSON Creator
- 퀴즈용 JSON 파일을 쉽게 생성
- 문제와 정답을 줄 단위로 입력

## 🚀 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone https://github.com/your-repo/HYUtestapp.git
cd HYUtestapp
```

### 2. 의존성 설치 (uv 사용)
```bash
uv sync
```

### 3. 환경 변수 설정
프로젝트 루트에 `.env` 파일을 생성하고 OpenAI API 키를 설정하세요:
```
OPENAI_API_KEY=your_api_key_here
```

> 💡 API 키는 [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.

### 4. 실행
```bash
uv run python main.py
```

## 📁 프로젝트 구조

```
HYUtestapp/
├── .env                 # API 키 설정 (직접 생성 필요)
├── .gitignore
├── pyproject.toml       # uv 프로젝트 설정
├── main.py              # 메인 런처
├── quiz_app.py          # Basic Quiz (정확 일치)
├── quiz_app_advanced.py # AI Quiz (OpenAI 채점)
├── json_creator.py      # JSON 파일 생성기
└── Questions/           # 퀴즈 문제 파일들
```

## 🎮 사용 방법

### 메인 런처
1. `main.py` 실행
2. 원하는 기능 선택:
   - **Basic Quiz**: 정확히 일치하는 답만 정답
   - **AI Quiz**: AI가 의미적으로 채점
   - **JSON Creator**: 문제 파일 생성

### JSON 파일 형식
```json
{
    "문제1": "정답1",
    "문제2": "정답2",
    "한국의 수도는?": "서울"
}
```

### AI 채점 예시
```
문제: 중국의 수도는 어디인가요?
정답: 베이징

✅ "베이징" → 정답
✅ "북경" → 정답 (AI가 동일 의미로 판단)
✅ "Beijing" → 정답 (AI가 동일 의미로 판단)
❌ "상하이" → 오답
```

## 🛠 기술 스택

- **Python 3.12+**
- **PyQt5** - GUI 프레임워크
- **OpenAI API** - AI 채점 (gpt-4.1-mini)
- **uv** - 패키지 관리
- **python-dotenv** - 환경 변수 관리

## 📝 의존성

```toml
[project]
dependencies = [
    "openai>=2.9.0",
    "pyqt5>=5.15.11",
    "python-dotenv>=1.2.1",
]
```

## 🤝 기여

이 프로젝트에 기여하고 싶다면 Pull Request를 보내주세요. 새로운 기능 추가, 버그 수정, 문서 개선 등 모든 기여를 환영합니다.

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 라이선스가 부여됩니다.
