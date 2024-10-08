# ⏰ 한글 시계 암호기

이 프로젝트는 한글 문장을 암호화하거나 복호화하는 **Streamlit** 애플리케이션입니다. 각 한글 음절의 **중성**과 **종성**을 시계 방향으로 한 칸씩 이동시켜 암호화하며, 시계 반대 방향으로 이동시켜 복호화하는 기능을 제공합니다.

## 🔧 주요 기능

- **암호화**: 입력된 한글 문장의 중성과 종성을 시계 방향으로 한 칸씩 이동시켜 암호화된 문장을 생성합니다.
- **복호화**: 암호화된 한글 문장을 입력하면 중성과 종성을 시계 반대 방향으로 이동시켜 원래 문장으로 복호화합니다.
- **사용 예시**: 암호화 및 복호화의 예시를 제공하여 사용자가 쉽게 이해할 수 있도록 돕습니다.
- **탭 구분**: 암호화와 복호화를 별도의 탭으로 분리하여 사용자가 원하는 작업을 쉽게 선택할 수 있습니다.

## 🛠️ 설치 방법

1. Python이 설치되어 있는지 확인합니다.
   - Python 3.7 이상을 권장합니다.

2. 프로젝트를 클론하거나 다운로드합니다.

   ```bash
   git clone https://github.com/brainer3220/hangul-clock-cipher.git
   ```

3. 프로젝트 디렉토리로 이동합니다.

   ```bash
   cd Korean-Clock-Cipher
   ```

4. 필요한 Python 패키지를 설치합니다.

   ```bash
   pip install -r requirements.txt
   ```

   - `requirements.txt` 파일이 없다면 `streamlit` 패키지를 직접 설치할 수도 있습니다:

     ```bash
     pip install streamlit
     ```

## 🚀 실행 방법

1. 아래 명령어를 실행하여 Streamlit 애플리케이션을 시작합니다.

   ```bash
   streamlit run index.py
   ```

2. 웹 브라우저에서 `http://localhost:8501`으로 접속하여 애플리케이션을 사용할 수 있습니다.

## 🧩 사용 방법

1. 애플리케이션이 실행되면, **암호화**와 **복호화** 탭이 표시됩니다.
2. 원하는 탭을 선택하여 문장을 입력하고, 버튼을 클릭하여 암호화 또는 복호화된 결과를 확인할 수 있습니다.

### 암호화 탭

- 암호화할 문장을 입력하고 **암호화** 버튼을 클릭하면, 중성과 종성이 한 칸씩 이동된 암호화된 문장이 결과로 표시됩니다.

### 복호화 탭

- 암호화된 문장을 입력하고 **복호화** 버튼을 클릭하면, 원래의 문장으로 복원된 결과가 표시됩니다.

## 📚 사용 예시

- **원문**: `이 시계 만큼은 넘겨줄수 없다`
- **암호화**: `의 시거 믄킴은 넘겨줄수 없다`
- **복호화**: `이 시계 만큼은 넘겨줄수 없다`

## 📄 파일 설명

- `index.py`: Streamlit 기반의 한글 시계 암호화 및 복호화 애플리케이션의 메인 코드 파일입니다.
- `README.md`: 이 파일로, 프로젝트에 대한 설명 및 설치, 사용 방법을 안내합니다.
- `requirements.txt`: 프로젝트 실행에 필요한 Python 패키지 목록이 포함되어 있습니다.

## ⚙️ 기술 스택

- **Python 3.x+**
- **Streamlit**: 웹 애플리케이션을 쉽게 구축할 수 있는 파이썬 프레임워크.

## 📝 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다.

## ✨ 기여

기여를 환영합니다!

---

©️ 2024 brainer. 모든 권리 보유.
