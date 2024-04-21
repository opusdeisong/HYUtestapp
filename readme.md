# Quiz App

Quiz App은 사용자가 JSON 파일에서 문제를 로드하여 퀴즈를 풀 수 있는 대화형 애플리케이션입니다. 이 애플리케이션은 Python과 PyQt5를 사용하여 개발되었습니다.

## 기능

- 사용자는 JSON 파일을 선택하여 해당 파일의 문제를 풀 수 있습니다.
- 사용자는 랜덤으로 선택된 문제를 풀고 정답을 입력하고 제출할 수 있습니다.
- 정답을 맞히면 해당 문제는 문제 목록에서 제거됩니다.
- 정답을 틀리면 정답이 표시되고 다음 문제로 넘어갑니다.
- 모든 문제를 풀면 퀴즈가 종료됩니다.

## JSON 생성 프로그램

별도의 JSON 생성 프로그램인 `json_creator.py`를 사용하여 퀴즈에 사용할 JSON 파일을 생성할 수 있습니다.

### 기능

- 사용자는 문제와 정답을 여러 줄 텍스트 형식으로 입력할 수 있습니다.
- "Create JSON" 버튼을 클릭하여 입력된 문제와 정답을 JSON 파일로 저장할 수 있습니다.
- 문제와 정답의 개수가 일치하지 않거나 입력된 데이터가 없는 경우 해당 오류 메시지가 표시됩니다.
- "Clear" 버튼을 클릭하여 입력 필드를 초기화할 수 있습니다.

## 추가 기능: 생성형 AI를 활용한 정답 판단

`quiz_app_advanced.py` 파일에는 생성형 AI를 활용하여 정답 판단을 개선한 버전의 Quiz App이 포함되어 있습니다. 이 버전에서는 Anthropic의 Claude API를 사용하여 주어진 답과 정답 간의 의미적 유사성을 판단합니다. 이를 통해 사용자의 답이 의미적으로 맞더라도 기존에는 틀렸다고 판단되던 문제를 해결할 수 있습니다.

생성형 AI를 활용하려면 다음 단계를 따르세요:

1. Anthropic에서 API 키를 발급받으세요.
2. `quiz_app_advanced.py` 파일에서 `YOUR_API_KEY` 부분을 실제 API 키로 대체하세요.
3. 필요한 라이브러리를 설치하세요: `pip install anthropic`

### 생성형 AI 정답 판단 예시

예를 들어, 다음과 같은 문제와 정답이 JSON 파일에 저장되어 있다고 가정해보겠습니다:

```
문제: 중국의 수도는 어디인가요?
정답: 베이징
```

사용자가 "북경"이라고 입력한 경우, 생성형 AI는 "베이징"과 "북경"이 의미적으로 동일한 것으로 판단하여 정답으로 인정합니다. 이렇게 생성형 AI를 활용하면 사용자의 다양한 표현을 이해하고 정답을 유연하게 판단할 수 있습니다.

## 필요한 라이브러리

- Python 3.x
- PyQt5
- anthropic (생성형 AI 버전에 필요)

## 설치 및 실행

1. 이 저장소를 클론하거나 ZIP 파일로 다운로드하세요.
2. 터미널 또는 명령 프롬프트를 열고 프로젝트 디렉토리로 이동하세요.
3. 다음 명령을 실행하여 필요한 라이브러리를 설치하세요:
   ```
   pip install PyQt5
   pip install anthropic (생성형 AI 버전에 필요)
   ```
4. 다음 명령을 실행하여 프로그램을 시작하세요:
   ```
   python main.py
   ```

## 사용 방법

1. `main.py` 파일을 실행하여 프로그램을 시작하세요.
2. 메인 창에서 원하는 프로그램을 선택하세요:
   - 'Start Quiz App' 버튼: 기본 버전의 Quiz App을 시작합니다.
   - 'Start Advanced Quiz App' 버튼: 생성형 AI를 활용한 개선된 버전의 Quiz App을 시작합니다.
   - 'Start JSON Creator' 버튼: JSON 생성 프로그램을 시작합니다.
3. 선택한 프로그램의 지시에 따라 퀴즈를 진행하거나 JSON 파일을 생성하세요.

### JSON 생성 프로그램

1. JSON 생성 프로그램에서 문제와 정답을 각각의 입력 필드에 입력하세요. 한 줄에 하나의 문제와 정답을 입력하세요.
2. "Create JSON" 버튼을 클릭하여 JSON 파일을 생성하세요.
3. 파일 저장 대화 상자에서 JSON 파일의 이름과 위치를 지정하고 저장하세요.

### Quiz App

1. Quiz App에서 JSON 파일을 선택하라는 메시지가 표시되면 생성한 JSON 파일을 선택하세요.
2. 랜덤으로 선택된 문제가 화면에 표시됩니다.
3. 정답을 입력 필드에 입력하고 'Submit' 버튼을 클릭하거나 엔터 키를 누르세요.
4. 정답이 맞으면 다음 문제로 자동으로 이동합니다. 정답이 틀리면 정답이 표시되고 다음 문제로 넘어갑니다.
5. 모든 문제를 풀면 퀴즈가 종료됩니다.

## 파일 구조

- `main.py`: 메인 프로그램 파일
- `quiz_app.py`: 기본 버전의 Quiz App 파일
- `quiz_app_advanced.py`: 생성형 AI를 활용한 개선된 버전의 Quiz App 파일
- `json_creator.py`: JSON 생성 프로그램 파일
- `questions.json`: 샘플 문제와 정답이 저장된 JSON 파일

## 기여

이 프로젝트에 기여하고 싶다면 Pull Request를 보내주세요. 새로운 기능 추가, 버그 수정, 문서 개선 등 모든 기여를 환영합니다.

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)에 따라 라이선스가 부여됩니다.