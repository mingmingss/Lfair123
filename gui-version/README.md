# 🎯 AI 광고 취향 분석기 - GUI 버전

마우스로 클릭하며 사용하는 그래픽 인터페이스 버전입니다.

## ✨ 주요 기능

- 📝 광고 문구 입력 및 평가
- 🤖 AI 기반 감성 분석 (KNU 한국어 감성사전 활용)
- 📊 광고 스타일 및 산업군 자동 분류
- 🧠 개인 취향 분석 및 통계
- ✨ 맞춤형 광고 카피 추천 (TF-IDF 유사도 기반)
- 🖱️ 직관적인 그래픽 사용자 인터페이스 (GUI)
- 📋 탭 기반 UI로 쉬운 네비게이션

---

## 📋 필요한 것

1. **Python 3.8 이상**
   - Python이 설치되어 있지 않다면 [python.org](https://www.python.org/downloads/)에서 다운로드하세요
   - **tkinter는 Python에 기본으로 포함되어 있어 별도 설치가 필요 없습니다!**

2. **필수 파일** (이 폴더에 모두 포함되어 있습니다)
   - `main_gui.py` - 메인 프로그램
   - `SentiWord_info.json` - 감성 분석용 사전
   - `ad_copy_database.json` - 광고 카피 데이터베이스
   - `requirements.txt` - 필요한 라이브러리 목록

---

## 🚀 설치 방법 (Python 초보자용)

### Windows 사용자

1. **Python 설치 확인**
   ```cmd
   python --version
   ```
   Python 버전이 표시되면 설치되어 있는 것입니다.

2. **이 폴더로 이동**
   - 파일 탐색기에서 `gui-version` 폴더를 열고
   - 주소창에 `cmd`를 입력하고 Enter를 누르면 이 폴더에서 명령 프롬프트가 열립니다

3. **필요한 라이브러리 설치**
   ```cmd
   python -m pip install --user -r requirements.txt
   ```

   또는 pip가 작동하지 않으면:
   ```cmd
   py -m pip install --user -r requirements.txt
   ```

4. **프로그램 실행**
   ```cmd
   python main_gui.py
   ```

   또는 더 쉬운 방법:
   - `main_gui.py` 파일을 더블클릭하면 바로 실행됩니다!

### Mac / Linux 사용자

1. **Python 설치 확인**
   ```bash
   python3 --version
   ```

2. **이 폴더로 이동**
   ```bash
   cd 경로/gui-version
   ```

3. **필요한 라이브러리 설치**
   ```bash
   python3 -m pip install --user -r requirements.txt
   ```

4. **프로그램 실행**
   ```bash
   python3 main_gui.py
   ```

---

## 📦 설치되는 라이브러리

- `scikit-learn` - 텍스트 유사도 분석 (TF-IDF, 코사인 유사도)
- `numpy` - 수치 계산

**참고**: `tkinter`는 Python에 기본으로 포함되어 있어 별도로 설치할 필요가 없습니다!

---

## 💡 사용 방법

### 1. 프로그램 실행
프로그램을 실행하면 GUI 창이 나타납니다.

### 2. 탭 메뉴
- **📝 광고 평가하기**: 광고 문구를 입력하고 AI 분석 후 평가
- **🧠 AI 취향 분석**: 평가한 광고들을 기반으로 나의 취향 분석
- **📋 평가 기록**: 지금까지 평가한 광고 목록 확인
- **✨ 맞춤 광고 추천**: AI가 나의 취향에 맞는 광고 카피 추천

### 3. 광고 평가하기
1. 광고 문구 입력란에 광고를 입력
2. "🤖 AI 분석하기" 버튼 클릭
3. 분석 결과 확인
4. 슬라이더로 평점 선택 (1-10점)
5. "💾 평가 저장하기" 버튼 클릭

### 4. 데이터 저장
평가 데이터는 `ad_data.json` 파일에 자동 저장됩니다.

---

## ⚠️ 문제 해결

### "No module named 'sklearn'" 오류가 나요
라이브러리 설치 단계를 다시 실행하세요:
```bash
python -m pip install --user -r requirements.txt
```

### "python을 찾을 수 없습니다" 오류가 나요
- Windows: `python` 대신 `py`를 사용하세요
- Mac/Linux: `python` 대신 `python3`을 사용하세요

### JSON 파일을 찾을 수 없다는 오류가 나요
`main_gui.py`, `SentiWord_info.json`, `ad_copy_database.json` 파일이 모두 같은 폴더에 있는지 확인하세요.

### 더블클릭해도 창이 바로 사라져요
1. 명령 프롬프트/터미널에서 실행하여 오류 메시지를 확인하세요
2. 대부분의 경우 라이브러리 설치가 필요합니다
3. 위의 설치 방법을 따라 라이브러리를 설치한 후 다시 실행하세요

### GUI 창이 너무 작거나 커요
- 창의 모서리를 마우스로 드래그하여 크기를 조절할 수 있습니다
- 프로그램이 자동으로 적절한 크기(1000x700)로 시작됩니다

### Linux에서 tkinter 오류가 나요
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

---

## 📝 참고사항

- 추천 기능은 최소 3개 이상의 광고를 평가한 후 사용할 수 있습니다
- 7점 이상 평가한 광고가 많을수록 더 정확한 추천을 받을 수 있습니다
- 평가 데이터는 프로그램을 종료해도 보존됩니다
- 여러 탭을 자유롭게 이동하며 사용할 수 있습니다

---

## 🆚 CLI 버전과의 차이점

| 특징 | CLI 버전 | GUI 버전 |
|------|----------|----------|
| 인터페이스 | 텍스트 기반 터미널 | 그래픽 기반 윈도우 |
| 사용 방법 | 키보드 입력 | 마우스 클릭 + 키보드 입력 |
| 화면 전환 | 순차적 메뉴 | 탭으로 자유롭게 이동 |
| 시각화 | Rich 라이브러리 | tkinter 위젯 |
| 실행 방법 | 터미널 필수 | 더블클릭 실행 가능 |

두 버전의 **핵심 기능과 알고리즘은 동일**하며, 인터페이스만 다릅니다!

---

## 📄 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.
