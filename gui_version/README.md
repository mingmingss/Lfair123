# 🎨 AI 광고 취향 분석기 - GUI 버전

Tkinter 기반의 그래픽 사용자 인터페이스(GUI) 버전입니다.
터미널이 익숙하지 않은 분들도 쉽게 사용할 수 있습니다!

## 빠른 시작 ⚡

### 방법 1: 가장 간단한 방법 (초보자 추천) ⭐

Python만 설치되어 있다면 바로 시작할 수 있습니다!

```bash
# 1. 프로젝트 폴더로 이동 (이미 다운로드했다면)
cd Lfair123

# 2. 필요한 라이브러리 설치 (처음 한 번만)
pip install -r requirements.txt
# 또는: pip3 install -r requirements.txt

# 3. GUI 버전 실행!
cd gui_version
python3 main_gui.py
```

### 방법 2: 가상환경 사용하기 (권장, 여러 프로젝트 관리 시)

여러 Python 프로젝트를 관리한다면 가상환경을 사용하세요.

```bash
# 1. 프로젝트 루트로 이동
cd Lfair123

# 2. 가상환경 생성 (처음 한 번만)
python3 -m venv .venv             # Windows: python -m venv .venv

# 3. 가상환경 활성화
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 4. 라이브러리 설치 (처음 한 번만)
pip install -r requirements.txt

# 5. GUI 실행
cd gui_version
python3 main_gui.py
```

## 필요한 것 📋

- **Python 3.12 이상**
- **필수 라이브러리**:
  - `rich>=13.0.0` (터미널 출력용)
  - `scikit-learn>=1.7.2` (TF-IDF, 유사도 계산)
  - `numpy>=2.3.5` (수치 연산)
  - `tkinter` (GUI, Python에 기본 포함됨)

### tkinter 설치 확인

대부분의 Python 설치에는 tkinter가 포함되어 있지만, 리눅스에서는 별도 설치가 필요할 수 있습니다:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS - 기본 포함됨
# Windows - 기본 포함됨
```

tkinter가 제대로 설치되었는지 확인:
```bash
python3 -c "import tkinter; print('tkinter 사용 가능!')"
```

## 주요 기능 ✨

### 탭 1: 📝 광고 평가하기
- 광고 문구 입력
- AI 자동 감성 분석
  - 감성 점수 및 라벨 (긍정/부정/중립/혼합)
  - 광고 스타일 분류 (유머형, 감성형, 정보형 등)
  - 산업군 추정 (IT, 패션뷰티, 식품음료 등)
  - 핵심 키워드 추출
  - 언어 패턴 분석
- 1-10점 평점 슬라이더
- 평가 저장

### 탭 2: 🧠 AI 취향 분석
- 감성 톤별 선호도 통계
- 광고 스타일별 평균 점수
- 최고/최저 평가 광고
- 개인화된 인사이트

### 탭 3: 📋 평가 기록
- 지금까지 평가한 모든 광고 목록
- 광고 문구, 평점, 감성 라벨 표시
- 테이블 형식으로 깔끔하게 정리

### 탭 4: ✨ 맞춤 광고 추천
- 내가 좋아한 광고 기반 AI 추천
- TF-IDF 유사도 분석
- 브랜드, 카테고리, 유사도 점수 표시
- 취향 분석 리포트

## 사용 방법 📖

1. **프로그램 실행**
   ```bash
   cd gui_version
   python3 main_gui.py
   ```

2. **첫 번째 광고 평가하기**
   - "📝 광고 평가하기" 탭 선택
   - 광고 문구 입력 (예: "당신의 행복을 위한 선택")
   - "🤖 AI 분석하기" 버튼 클릭
   - 분석 결과 확인
   - 슬라이더로 1-10점 평점 선택
   - "💾 평가 저장하기" 버튼 클릭

3. **취향 분석 보기**
   - 광고를 3개 이상 평가한 후
   - "🧠 AI 취향 분석" 탭 선택
   - "🔄 취향 분석 새로고침" 버튼 클릭

4. **맞춤 추천 받기**
   - 광고를 3개 이상 평가하고, 7점 이상 준 광고가 있다면
   - "✨ 맞춤 광고 추천" 탭 선택
   - "🎯 나에게 맞는 광고 카피 추천받기" 버튼 클릭

## 데이터 파일 위치 📁

```
gui_version/
├── main_gui.py          # GUI 메인 프로그램
└── README.md            # 이 파일

../script/               # 데이터 파일 위치
├── SentiWord_info.json      # KNU 한국어 감성사전
├── ad_data.json             # 내가 평가한 광고 데이터
└── ad_copy_database.json    # 추천용 광고 카피 DB
```

> **참고**: GUI 버전과 터미널 버전(script/main2.py)은 같은 데이터 파일을 공유합니다.
> 어느 버전에서 평가하든 데이터가 누적됩니다!

## 문제 해결 🔧

### "tkinter를 찾을 수 없습니다" 오류
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS - Python을 python.org에서 다시 설치
# Windows - Python을 재설치할 때 "tcl/tk and IDLE" 옵션 체크
```

### "No module named 'sklearn'" 오류
```bash
pip install scikit-learn
```

### "No module named 'rich'" 오류
```bash
pip install rich
```

### 모든 의존성 한 번에 설치
```bash
cd ..  # Lfair123 폴더로 이동
pip install -r requirements.txt
```

### 창이 너무 작게 보여요
- 프로그램 실행 후 창 크기를 조절할 수 있습니다
- 또는 `main_gui.py` 파일에서 239번째 줄의 `self.root.geometry("1000x700")`을 원하는 크기로 수정하세요

## 터미널 버전과 비교 🔄

| 특징 | GUI 버전 | 터미널 버전 (main2.py) |
|------|---------|----------------------|
| 사용 편의성 | ⭐⭐⭐⭐⭐ 마우스로 클릭 | ⭐⭐⭐ 키보드 입력 |
| 시각적 아름다움 | ⭐⭐⭐⭐ 깔끔한 GUI | ⭐⭐⭐⭐⭐ Rich 컬러 UI |
| 속도 | ⭐⭐⭐⭐ 빠름 | ⭐⭐⭐⭐⭐ 매우 빠름 |
| 추천 대상 | Python 초보자 | 개발자, 터미널 사용자 |

## 개발자 정보 👨‍💻

- GUI는 Python 표준 라이브러리인 Tkinter로 개발되었습니다
- 감성 분석은 KNU 한국어 감성사전을 기반으로 합니다
- 추천 시스템은 scikit-learn의 TF-IDF와 코사인 유사도를 사용합니다
- Original version: `/script/main2.py`를 기반으로 제작되었습니다

## 더 알아보기 📚

- 메인 프로젝트 README: `../README.md`
- 터미널 버전 (Rich UI): `../script/main2.py`
- 간단한 콘솔 버전: `../script/main1.py`

---

**즐거운 광고 분석 되세요!** 🎉
