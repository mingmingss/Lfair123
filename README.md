# Lfair123

한국어 광고 문구 감성 분석 프로젝트

## 프로젝트 소개

이 프로젝트는 KNU 한국어 감성사전을 기반으로 광고 문구의 감성을 분석하는 AI 도구입니다. **Kiwipiepy** 형태소 분석기와 **Rich** 터미널 UI를 활용하여 정확하고 아름다운 분석 결과를 제공합니다.

### 주요 기능

- **🔬 고급 형태소 분석**: Kiwipiepy를 활용한 정확한 한국어 토큰화 및 의미 추출
- **📊 감성 분석**: KNU 한국어 감성사전 기반 정밀 감성 점수 산출
- **🎨 광고 스타일 분류**: 유머형, 감성형, 정보형, 긴급형, 프리미엄형 등 11가지 스타일 자동 분류
- **🏢 산업군 분류**: 기술IT, 패션뷰티, 식품음료, 건강의료 등 8가지 산업군 자동 분류
- **🔑 키워드 추출**: 형태소 기반 핵심 감성 키워드 자동 추출
- **💬 언어 패턴 분석**: 텍스트 길이, 단어 수, 이모지 사용 등 언어적 특징 분석
- **⚡ 감성 충돌 감지**: 긍정어와 부정어의 혼합 사용 패턴 감지 및 분석
- **✨ 아름다운 UI**: Rich 라이브러리 기반 컬러풀한 터미널 인터페이스

### 버전 정보

- **v1.0 (main1.py)**: 기본 버전 - 정규식 기반 단순 분석
- **v4.0 (main2.py)**: 개선 버전 - Kiwipiepy 형태소 분석 + Rich UI (권장)

## 설치 방법

### UV를 사용하는 경우 (권장)

[UV](https://github.com/astral-sh/uv)는 빠르고 현대적인 Python 패키지 관리자입니다.

1. UV 설치 (아직 설치하지 않은 경우)
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. 프로젝트 클론 및 설정
   ```bash
   git clone https://github.com/mingmingss/Lfair123.git
   cd Lfair123

   # 가상환경 생성 및 의존성 설치
   uv venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

### UV를 사용하지 않는 경우

일반적인 Python pip를 사용하는 방법입니다.

1. 프로젝트 클론
   ```bash
   git clone https://github.com/mingmingss/Lfair123.git
   cd Lfair123
   ```

2. 가상환경 생성 (권장)
   ```bash
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. 의존성 설치
   ```bash
   pip install -e .
   ```

## 사용 방법

### 개선 버전 실행 (권장)

형태소 분석과 Rich UI가 적용된 최신 버전:

```bash
cd script
python3 main2.py
```

### 기본 버전 실행

기본 정규식 기반 버전:

```bash
cd script
python3 main1.py
```

## 주요 기능

### 1. 광고 평가하기
- 광고 문구를 입력하면 자동으로 AI 감성 분석을 수행합니다
- 형태소 분석 결과, 감성 점수, 광고 스타일, 산업군 등이 표시됩니다
- 분석 결과를 확인한 후 평점(1-10)을 입력할 수 있습니다

### 2. AI 취향 분석 보기
- 저장된 모든 광고 데이터를 기반으로 당신의 광고 취향을 분석합니다
- 감성 톤 선호도, 광고 스타일 선호도를 테이블로 확인할 수 있습니다
- 베스트/워스트 광고를 자동으로 추천합니다

### 3. 평가 기록 보기
- 지금까지 평가한 모든 광고를 테이블 형식으로 확인할 수 있습니다
- 각 광고의 평점, 감성 라벨이 한눈에 표시됩니다

## 개선 사항 (v4.0)

### 🔬 형태소 분석 (Kiwipiepy)
- **이전**: 정규식으로 단순 단어 추출 (`re.findall(r'[가-힣]+', text)`)
- **개선**: 한국어 형태소 분석기로 정확한 토큰화
  - "먹었다" → "먹"(동사) + "었"(어미) + "다"(어미) 올바르게 분리
  - 조사, 어미 제거로 정확한 키워드 매칭
  - 품사 정보 활용 (명사, 동사, 형용사만 추출)

### ✨ Rich UI
- **이전**: 기본 print() 흑백 텍스트
- **개선**: 컬러풀하고 구조화된 터미널 UI
  - 색상으로 감성 점수 표현 (긍정=녹색, 부정=빨간색)
  - 테이블로 통계 데이터 표시
  - 패널, 프로그레스 바 등 직관적인 UI

## 데이터 파일

- `script/SentiWord_info.json`: KNU 한국어 감성사전 데이터
- `script/ad_data.json`: 분석된 광고 데이터 저장 파일

## 요구사항

- Python 3.12 이상
- kiwipiepy >= 0.18.0 (한국어 형태소 분석)
- rich >= 13.0.0 (터미널 UI)

## 프로젝트 구조

```
Lfair123/
├── script/
│   ├── main1.py              # 기본 버전 (정규식 기반)
│   ├── main2.py              # 개선 버전 (Kiwipiepy + Rich)
│   ├── SentiWord_info.json   # KNU 한국어 감성사전
│   └── ad_data.json          # 사용자 광고 데이터 (자동 생성)
├── pyproject.toml            # 프로젝트 설정 및 의존성
├── uv.lock                   # UV 의존성 락 파일
└── README.md                 # 프로젝트 문서
```

## 라이선스

이 프로젝트는 교육 및 연구 목적으로 사용됩니다.

## 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.
