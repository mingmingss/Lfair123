# 🎯 AI 광고 취향 분석기 (Lfair123)

AI 기반 한국어 광고 감성·취향 분석 애플리케이션

광고 카피를 입력하고 감성·스타일을 분석해 나만의 취향 프로필과 맞춤 광고 카피를 추천받으세요!

---

## ✨ 주요 기능

- 🤖 **AI 감성 분석**: KNU 한국어 감성사전 기반 정교한 감성 점수 계산
- 🎨 **광고 스타일 분류**: 유머형, 감성형, 정보형 등 11가지 스타일 자동 분류
- 🏢 **산업군 추정**: IT, 패션뷰티, 식품음료 등 8개 산업군 자동 인식
- 🔑 **핵심 키워드 추출**: 감성 강도가 높은 키워드 자동 추출
- 🧠 **AI 취향 분석**: 내가 평가한 광고를 기반으로 취향 프로필 생성
- 💡 **맞춤형 추천**: TF-IDF 유사도 기반 개인화 광고 카피 추천
- 🔍 **유사 광고 검색**: 과거 평가한 광고 중 유사한 광고 자동 탐색

---

## 📂 프로젝트 구조

```
Lfair123/
├── README.md                    # 프로젝트 전체 설명 (이 파일)
│
├── cli-version/                 # 터미널 버전 (독립 실행 가능)
│   ├── main2.py                 # 메인 프로그램
│   ├── SentiWord_info.json      # 감성사전
│   ├── ad_copy_database.json    # 광고 카피 DB
│   ├── requirements.txt         # 필요한 라이브러리
│   └── README.md                # CLI 버전 설치/사용 가이드
│
└── gui-version/                 # GUI 버전 (독립 실행 가능)
    ├── main_gui.py              # 메인 프로그램
    ├── SentiWord_info.json      # 감성사전
    ├── ad_copy_database.json    # 광고 카피 DB
    ├── requirements.txt         # 필요한 라이브러리
    └── README.md                # GUI 버전 설치/사용 가이드
```

> 💡 **독립적인 폴더 구조**: 각 폴더(`cli-version`, `gui-version`)를 따로 다운로드해서 독립적으로 사용할 수 있습니다!

---

## 🚀 빠른 시작

### 1️⃣ CLI 버전 (터미널)

터미널에서 아름다운 UI로 사용하는 버전입니다.

```bash
# 1. CLI 버전 폴더로 이동
cd cli-version

# 2. 라이브러리 설치
python -m pip install --user -r requirements.txt

# 3. 실행!
python main2.py
```

**추천 대상**: 개발자, 터미널 사용자, Rich UI를 선호하는 분

📖 [자세한 설치 가이드 →](cli-version/README.md)

---

### 2️⃣ GUI 버전 (그래픽 인터페이스)

마우스로 클릭하며 사용하는 GUI 버전입니다.

```bash
# 1. GUI 버전 폴더로 이동
cd gui-version

# 2. 라이브러리 설치
python -m pip install --user -r requirements.txt

# 3. 실행!
python main_gui.py
```

또는 **`main_gui.py` 파일을 더블클릭**하면 바로 실행됩니다!

**추천 대상**: Python 초보자, GUI를 선호하는 분

📖 [자세한 설치 가이드 →](gui-version/README.md)

---

## 🔧 필요한 것

- **Python 3.8 이상** ([다운로드](https://www.python.org/downloads/))
- **필요한 라이브러리**:
  - `rich` - 아름다운 터미널 UI (CLI 버전만)
  - `scikit-learn` - 텍스트 유사도 분석
  - `numpy` - 수치 계산
  - `tkinter` - GUI (Python에 기본 포함, 별도 설치 불필요)

> 💡 라이브러리는 각 폴더의 `requirements.txt`를 통해 자동으로 설치됩니다!

---

## 📊 두 버전 비교

| 특징 | CLI 버전 | GUI 버전 |
|------|----------|----------|
| **인터페이스** | 텍스트 기반 터미널 | 그래픽 기반 윈도우 |
| **사용 방법** | 키보드 입력 | 마우스 클릭 + 키보드 |
| **화면 전환** | 순차적 메뉴 | 탭으로 자유롭게 이동 |
| **시각화** | Rich 라이브러리 (컬러풀) | tkinter 위젯 |
| **실행 방법** | 터미널 필수 | 더블클릭 실행 가능 |
| **속도** | ⭐⭐⭐⭐⭐ 매우 빠름 | ⭐⭐⭐⭐ 빠름 |
| **사용 편의성** | ⭐⭐⭐ 키보드 숙련 필요 | ⭐⭐⭐⭐⭐ 직관적 |

**핵심 기능과 알고리즘은 동일**하며, 인터페이스만 다릅니다. 취향에 맞는 버전을 선택하세요!

---

## 💡 사용 흐름

### 1. 광고 평가하기
- 광고 문구를 입력하면 즉시 AI 감성 분석 결과를 확인
- 감성 점수, 광고 스타일, 산업군, 핵심 키워드 등이 표시됨
- 1-10점으로 평가하면 자동으로 저장

### 2. AI 취향 분석
- 평가한 광고들을 기반으로 나의 취향 프로필 생성
- 감성 톤별/스타일별 선호도 통계
- 최고 평가 광고 vs 최저 평가 광고

### 3. 평가 기록 보기
- 지금까지 평가한 모든 광고 목록
- 광고 문구, 평점, 감성 라벨 확인

### 4. 맞춤 광고 카피 추천
- 내가 좋아한 광고(7점 이상)를 기반으로 AI 추천
- TF-IDF 유사도 분석으로 나에게 맞는 광고 카피 제안
- 브랜드, 카테고리, 유사도 점수 표시

---

## 🎓 초보자를 위한 설치 가이드

### Windows 사용자

1. **Python 설치 확인**
   - Windows 검색에서 "cmd" 입력 후 명령 프롬프트 실행
   - `python --version` 입력 후 Enter
   - 버전이 표시되면 설치됨, 아니면 [python.org](https://www.python.org/downloads/)에서 다운로드

2. **원하는 버전 폴더로 이동**
   - 파일 탐색기에서 `cli-version` 또는 `gui-version` 폴더 열기
   - 주소창에 `cmd` 입력 후 Enter

3. **라이브러리 설치**
   ```cmd
   python -m pip install --user -r requirements.txt
   ```

4. **실행**
   ```cmd
   python main2.py          (CLI 버전)
   python main_gui.py       (GUI 버전)
   ```

### Mac / Linux 사용자

1. **Python 설치 확인**
   ```bash
   python3 --version
   ```

2. **원하는 버전 폴더로 이동**
   ```bash
   cd 다운로드/Lfair123/cli-version    # 또는 gui-version
   ```

3. **라이브러리 설치**
   ```bash
   python3 -m pip install --user -r requirements.txt
   ```

4. **실행**
   ```bash
   python3 main2.py         # CLI 버전
   python3 main_gui.py      # GUI 버전
   ```

---

## 🔍 핵심 기술

### 감성 분석
- **KNU 한국어 감성사전** 기반
- 단어별 극성 점수를 활용한 정교한 감성 계산
- 혼합 감성 감지 (긍정+부정 동시 포함)

### 광고 추천
- **TF-IDF** (Term Frequency-Inverse Document Frequency)
- **코사인 유사도** (Cosine Similarity)
- scikit-learn 라이브러리 활용

### 스타일 분류
- 정규식 기반 키워드 매칭
- 11가지 광고 스타일: 유머형, 감성형, 정보형, 긴급형, 프리미엄형, 실용형, 도전형 등
- 8가지 산업군: IT, 패션뷰티, 식품음료, 건강의료, 금융서비스, 여행레저, 자동차, 가전홈

---

## 📝 데이터 파일 설명

- **`SentiWord_info.json`**: KNU 한국어 감성사전 (약 118만 개 단어)
- **`ad_copy_database.json`**: 추천용 광고 카피 데이터베이스
- **`ad_data.json`**: 사용자가 평가한 광고 저장 (자동 생성)

---

## ⚠️ 문제 해결

### 자주 묻는 질문

**Q: "python을 찾을 수 없습니다" 오류가 나요**
- Windows: `python` 대신 `py` 사용
- Mac/Linux: `python` 대신 `python3` 사용

**Q: "No module named 'sklearn'" 오류가 나요**
```bash
python -m pip install --user -r requirements.txt
```

**Q: GUI 버전을 더블클릭해도 바로 사라져요**
- 명령 프롬프트/터미널에서 실행하여 오류 확인
- 대부분 라이브러리 미설치 문제

**Q: 한글이 깨져 보여요**
- Windows: 명령 프롬프트 속성 → 글꼴 → "맑은 고딕" 선택
- 또는 `chcp 65001` 명령 실행 후 프로그램 재실행

자세한 문제 해결은 각 버전의 README를 참고하세요!

---

## 📖 더 알아보기

- [CLI 버전 상세 가이드](cli-version/README.md)
- [GUI 버전 상세 가이드](gui-version/README.md)

---

## 📄 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.

---

**즐거운 광고 분석 되세요!** 🎉
