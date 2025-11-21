# 🎯 AI 광고 취향 분석기 v4.0 GUI

Main2.py를 기반으로 한 GUI 버전입니다!

## 📋 기능

1. **📝 광고 평가하기**
   - 광고 문구 입력 및 AI 자동 분석
   - 감성 분석, 광고 스타일, 산업군 분류
   - 10점 만점 평가 시스템

2. **🧠 AI 취향 분석**
   - 감성 톤 선호도 분석
   - 광고 스타일 선호도 분석
   - 베스트/워스트 광고 확인

3. **📋 평가 기록**
   - 평가한 모든 광고 목록 확인
   - 평점 및 감성 정보 표시

4. **✨ 맞춤 광고 추천**
   - TF-IDF 기반 유사도 분석
   - 개인 취향에 맞는 광고 카피 추천

## 🚀 실행 방법

```bash
python main_gui.py
```

## 📦 필요한 라이브러리

```bash
pip install tkinter scikit-learn numpy
```

## 📁 파일 구조

```
gui_version/
├── main_gui.py          # GUI 메인 프로그램
└── README.md           # 설명서

../script/              # 데이터 파일 위치
├── SentiWord_info.json      # 감성사전
├── ad_data.json             # 평가 데이터
└── ad_copy_database.json    # 광고 카피 DB
```

## 💡 사용 팁

- 광고를 3개 이상 평가하면 맞춤 추천을 받을 수 있습니다
- 7점 이상 평가한 광고를 기반으로 추천이 이루어집니다
- 분석 결과는 자동으로 저장됩니다

## 🎨 UI 특징

- Tkinter 기반의 직관적인 GUI
- 탭 구조로 기능별 화면 분리
- 스크롤 가능한 텍스트 영역
- 슬라이더로 편리한 평점 입력

## 🔧 기술 스택

- Python 3.x
- Tkinter (GUI)
- scikit-learn (TF-IDF, 유사도 분석)
- NumPy (수치 계산)

## 📝 Original Version

이 GUI 버전은 `/script/main2.py`를 기반으로 제작되었습니다.
