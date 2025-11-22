# Lfair123

AI 기반 한국어 광고 감성·취향 분석기

## 프로젝트 한눈에 보기
- **목적**: 광고 카피를 입력하고 감성·스타일을 분석해 나만의 취향 프로필과 추천 카피를 제공하는 애플리케이션
- **핵심 기술**: KNU 한국어 감성사전 기반 감성 점수 + 정규식 토큰화, scikit-learn TF-IDF/코사인 유사도, Rich 컬러 CLI
- **데이터 흐름**: `ad_data.json`에 사용자가 평가한 광고가 누적되고, `ad_copy_database.json`은 추천용 레퍼런스 카피를 제공
- **실행 모드**:
  - `script/main2.py` (권장, Rich UI 터미널 버전)
  - `gui_version/main_gui.py` (GUI 버전)
  - `script/main1.py` (기본 콘솔 버전)

## 기능 하이라이트
- **정교한 감성 분석**: KNU 감성사전에서 단어 극성을 찾아 평균 점수, 긍/부정 키워드, 혼합 감성 여부를 계산합니다.
- **광고 스타일 및 산업군 추정**: 사전에 정의된 키워드를 사용해 유머형·감성형 등 11개 스타일과 8개 산업군을 스코어링합니다.
- **언어 패턴 리포트**: 문장 길이, 질문/감탄, 이모티콘 여부 등을 통해 광고의 표현 톤을 요약합니다.
- **AI 취향 리포트**: 감성 톤·광고 스타일별 선호도, 최고/최저 광고를 테이블로 시각화합니다.
- **유사 광고 검색**: 저장된 평가 내역을 TF-IDF로 임베딩하여 입력 광고와 비슷한 카피를 알려주고 평점 힌트를 제공합니다.
- **맞춤 광고 추천**: 내가 7점 이상 준 광고를 기반으로 `ad_copy_database.json`의 카피 중 유사한 문구를 추천합니다.
- **Rich UI**: 패널과 테이블, 색상 하이라이트로 분석 흐름과 메뉴가 명확하게 보이도록 구성했습니다.

## 시스템 구성
```
Lfair123/
├── README.md
├── requirements.txt        # pip 의존성 목록
├── pyproject.toml          # 프로젝트 메타데이터, 의존성 (rich, numpy, scikit-learn)
├── uv.lock                 # uv 사용 시 의존성 잠금
├── gui_version/
│   └── main_gui.py         # Tkinter 기반 GUI 버전
└── script/
    ├── main1.py            # 콘솔 기반 기본 버전
    ├── main2.py            # Rich UI + 추천 시스템 포함 (권장 실행)
    ├── SentiWord_info.json # KNU 한국어 감성사전 (필수 데이터)
    ├── ad_copy_database.json # 추천용 레퍼런스 광고 카피
    └── ad_data.json        # 사용자가 평가한 광고 내역 (실행 시 자동 생성/갱신)
```

### 주요 클래스
- `AdvancedSentimentAnalyzer`: 감성사전 로드 → 단어 추출(`re.findall`) → 감성 점수, 키워드, 스타일/산업군, 언어 패턴, 감성 충돌 정보를 계산합니다.
- `AdPreferenceAnalyzer`: 광고 입력/평가, 데이터 저장, 유사 광고 탐색, 개인화 추천, 취향 리포트, 히스토리 UI를 담당합니다.

## 설치

### 방법 1: UV 사용 (권장)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS/Linux
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

git clone https://github.com/mingmingss/Lfair123.git
cd Lfair123

uv venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv pip install -e .
```

### 방법 2: pip + requirements.txt
```bash
git clone https://github.com/mingmingss/Lfair123.git
cd Lfair123

python3 -m venv .venv             # Windows: python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 방법 3: pip + pyproject.toml
```bash
git clone https://github.com/mingmingss/Lfair123.git
cd Lfair123

python3 -m venv .venv             # Windows: python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

> **요구 사항**:
> - Python 3.12 이상
> - 의존성: `rich>=13.0.0`, `scikit-learn>=1.7.2`, `numpy>=2.3.5`
> - GUI 버전 실행 시 tkinter 필요 (Python 표준 라이브러리, 대부분의 Python 설치에 포함됨)

## 실행 방법

### 1. Rich UI 터미널 버전 (권장)
```bash
cd script
python3 main2.py
```
터미널에서 컬러풀한 Rich UI로 광고를 평가하고 분석합니다.

### 2. GUI 버전
```bash
cd gui_version
python3 main_gui.py
```
Tkinter 기반 GUI 애플리케이션으로 더 직관적인 인터페이스를 제공합니다.

### 3. 단순 콘솔 버전
```bash
cd script
python3 main1.py
```
기본 콘솔 인터페이스로 가장 단순한 형태입니다.

> **참고**: 첫 실행 시 `script/ad_data.json`이 없으면 자동으로 생성되고, 이후 광고 평가 내역이 계속 누적됩니다.

## 사용 흐름 (main2.py)
1. **광고 평가하기**
   - 광고 문구를 입력하면 즉시 감성 분석, 스타일 추정, 언어 패턴, 키워드 등이 Rich 패널로 표시됩니다.
   - 기존 평가 중 TF-IDF 코사인 유사도가 0.1 이상인 광고를 찾아 평점 힌트를 제공합니다.
   - 사용자가 1~10점 사이의 평점을 입력하면 `ad_data.json`에 저장됩니다.
2. **AI 취향 분석 보기**
   - 감성 톤별 평균 점수, 스타일별 선호도, 평가 건수, 최고/최저 광고를 컬러 테이블로 확인할 수 있습니다.
3. **평가 기록 보기**
   - 지금까지 입력한 광고, 평점, 감성 라벨을 번호순으로 보여줍니다.
4. **맞춤 광고 카피 추천**
   - 내가 7점 이상 준 광고 텍스트를 평균 벡터로 만들어 `ad_copy_database.json`과 비교한 뒤 상위 N개 카피를 추천합니다.

## 데이터 파일 설명
- `script/SentiWord_info.json`  
  - KNU 한국어 감성사전 원본(단어, 극성). 필요 시 최신 사전으로 교체 후 동일한 필드(`word`, `polarity`)를 유지하면 됩니다.
- `script/ad_copy_database.json`  
  - 브랜드, 카테고리, 카피 텍스트 목록. 추천 품질을 높이고 싶다면 같은 구조로 문구를 추가하세요.
- `script/ad_data.json`  
  - 다음과 같은 구조로 사용자 평가가 누적됩니다:
    ```json
    {
      "ad_text": "...",
      "overall_rating": 8,
      "sentiment_analysis": {
        "score": 0.75,
        "sentiment_label": "긍정",
        "ad_styles": [["감성형", 2]],
        "industries": [["패션뷰티", 1]],
        "keywords": [["사랑", 2]],
        "language_pattern": {...},
        "sentiment_conflict": {...},
        "words": ["사랑", "빛나는", "..."]
      },
      "timestamp": "2024-11-22T00:00:00"
    }
    ```

## 개발 메모
- 감성 분석은 정규식으로 추출한 한글/영문 토큰에 한해 감성사전과 매칭합니다. 필요 시 형태소 분석기를 붙이고 `AdvancedSentimentAnalyzer.extract_words`만 교체하면 됩니다.
- 유사 광고 탐색과 추천 기능은 `scikit-learn`의 `TfidfVectorizer`와 `cosine_similarity`를 사용하며, 유사도 임계값(기본 0.1)을 조정하면 더 엄격한 추천을 만들 수 있습니다.
- CLI는 Rich의 `Console`, `Table`, `Panel`, `Prompt`를 활용했습니다. UI를 커스터마이징하려면 `display_*` 메서드를 참고하세요.

## 기여 & 문의
- 버그 제보나 아이디어는 이슈로 남겨주세요.
- 데이터나 추천 알고리즘을 확장하고 싶다면 PR 환영합니다.
