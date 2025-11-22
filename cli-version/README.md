# 🎯 AI 광고 취향 분석기 - CLI 버전

터미널(명령 프롬프트)에서 사용하는 광고 취향 분석 프로그램입니다.

## ✨ 주요 기능

- 📝 광고 문구 입력 및 평가
- 🤖 AI 기반 감성 분석 (KNU 한국어 감성사전 활용)
- 📊 광고 스타일 및 산업군 자동 분류
- 🧠 개인 취향 분석 및 통계
- ✨ 맞춤형 광고 카피 추천 (TF-IDF 유사도 기반)
- 🎨 Rich 라이브러리를 활용한 아름다운 터미널 UI

---

## 📋 필요한 것

1. **Python 3.8 이상**
   - Python이 설치되어 있지 않다면 [python.org](https://www.python.org/downloads/)에서 다운로드하세요

2. **필수 파일** (이 폴더에 모두 포함되어 있습니다)
   - `main2.py` - 메인 프로그램
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
   - 파일 탐색기에서 `cli-version` 폴더를 열고
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
   python main2.py
   ```

### Mac / Linux 사용자

1. **Python 설치 확인**
   ```bash
   python3 --version
   ```

2. **이 폴더로 이동**
   ```bash
   cd 경로/cli-version
   ```

3. **필요한 라이브러리 설치**
   ```bash
   python3 -m pip install --user -r requirements.txt
   ```

4. **프로그램 실행**
   ```bash
   python3 main2.py
   ```

---

## 📦 설치되는 라이브러리

- `rich` - 아름다운 터미널 UI
- `scikit-learn` - 텍스트 유사도 분석 (TF-IDF, 코사인 유사도)
- `numpy` - 수치 계산

---

## 💡 사용 방법

1. 프로그램을 실행하면 메인 메뉴가 나타납니다
2. 원하는 메뉴 번호를 입력하세요:
   - `1` - 광고 평가하기: 광고 문구를 입력하고 AI 분석 결과를 확인한 후 평가
   - `2` - AI 취향 분석 보기: 평가한 광고들을 기반으로 나의 취향 분석
   - `3` - 평가 기록 보기: 지금까지 평가한 광고 목록
   - `4` - 맞춤 광고 카피 추천 받기: AI가 나의 취향에 맞는 광고 카피 추천
   - `5` - 종료

3. 평가 데이터는 `ad_data.json` 파일에 자동 저장됩니다

---

## ⚠️ 문제 해결

### "No module named 'rich'" 오류가 나요
라이브러리 설치 단계를 다시 실행하세요:
```bash
python -m pip install --user -r requirements.txt
```

### "python을 찾을 수 없습니다" 오류가 나요
- Windows: `python` 대신 `py`를 사용하세요
- Mac/Linux: `python` 대신 `python3`을 사용하세요

### JSON 파일을 찾을 수 없다는 오류가 나요
`main2.py`, `SentiWord_info.json`, `ad_copy_database.json` 파일이 모두 같은 폴더에 있는지 확인하세요.

### 한글이 깨져 보여요
- Windows: 명령 프롬프트 창 상단을 우클릭 → 속성 → 글꼴에서 "굴림" 또는 "맑은 고딕"으로 변경
- 터미널에서 `chcp 65001` 명령을 실행한 후 프로그램을 다시 실행

---

## 📝 참고사항

- 추천 기능은 최소 3개 이상의 광고를 평가한 후 사용할 수 있습니다
- 7점 이상 평가한 광고가 많을수록 더 정확한 추천을 받을 수 있습니다
- 평가 데이터는 프로그램을 종료해도 보존됩니다

---

## 📄 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.
