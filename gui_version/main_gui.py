import json
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import re
from typing import List, Dict, Tuple

# 텍스트 유사도 분석 및 머신러닝
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class AdvancedSentimentAnalyzer:
    """KNU 한국어 감성사전 기반 감성 분석기"""

    def __init__(self, senti_dict_path="SentiWord_info.json"):
        self.sentiment_dict = {}

        # 감성사전 파일 경로 찾기 (유연한 경로 탐색)
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 1순위: 현재 디렉토리
        # 2순위: ../script/ 디렉토리
        possible_paths = [
            os.path.join(script_dir, senti_dict_path),
            os.path.join(os.path.dirname(script_dir), "script", senti_dict_path)
        ]

        full_path = None
        for path in possible_paths:
            if os.path.exists(path):
                full_path = path
                break

        if full_path is None:
            full_path = possible_paths[0]  # 기본값

        self.load_sentiment_dict(full_path)

        # 광고 스타일 키워드 사전 (확장)
        self.style_keywords = {
            '유머형': ['ㅋ', 'ㅎ', '웃', '재미', '유머', '우습', '깔깔', '하하'],
            '감성형': ['마음', '사랑', '행복', '따뜻', '소중', '감동', '추억', '함께', '가족', '일상', '순간'],
            '정보형': ['새로운', '최초', '기술', '혁신', '특허', '개발', '성분', '효과', '과학'],
            '긴급형': ['지금', '오늘', '한정', '마지막', '서둘', '빨리', '곧', '즉시', '바로'],
            '프리미엄형': ['프리미엄', '럭셔리', '고급', '명품', '최고급', '특별', '한정판', '격'],
            '실용형': ['편리', '간편', '실용', '유용', '효율', '절약', '알뜸', '가성비', '쉽', '빠른'],
            '도전형': ['도전', '극복', '성취', '꿈', '목표', '열정', '성공', '이루', '시작', '변화'],
            '언어유희형': ['친구', '팀', '국룰', '케미', '통역'],
            '건강웰빙형': ['건강', '피로', '상처', '통증', '영양', '케어'],
            '라이프형': ['스타일', '삶', '생활', '디자인', '취향', '나답', '매일'],
            '혁신기술형': ['AI', '혁신', '미래', '성장', '발전', '진화', '스마트']
        }

        # 산업군 키워드 사전
        self.industry_keywords = {
            '기술IT': ['AI', '기술', '혁신', '앱', '데이터', '전자', '스마트', '디지털'],
            '패션뷰티': ['스타일', '패션', '옷', '뷰티', '화장', '피부'],
            '식품음료': ['맛', '먹', '음식', '커피', '술', '음료', '식품'],
            '건강의료': ['건강', '의료', '치료', '약', '병원', '운동', '다이어트'],
            '금융서비스': ['은행', '카드', '보험', '금융', '투자', '적립'],
            '여행레저': ['여행', '휴가', '레저', '관광', '호텔', '항공'],
            '자동차': ['차', '자동차', '운전', '엔진', '주행'],
            '가전홈': ['가전', '집', '홈', '가구', '생활', '청소']
        }

    def load_sentiment_dict(self, filepath):
        """감성사전 로드"""
        if not os.path.exists(filepath):
            print(f"⚠️  감성사전 파일({filepath})을 찾을 수 없습니다.")
            print("감성 분석 기능이 비활성화됩니다.")
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 단어: 극성 매핑
            for item in data:
                word = item['word']
                polarity = int(item['polarity'])
                self.sentiment_dict[word] = polarity

            print(f"✅ 감성사전 로드 완료: {len(self.sentiment_dict):,}개 단어")
        except Exception as e:
            print(f"⚠️  감성사전 로드 실패: {e}")

    def extract_words(self, text: str) -> List[str]:
        """텍스트에서 단어 추출 (한글, 영어)"""
        return re.findall(r'[가-힣]+|[a-zA-Z]+', text)

    def classify_ad_style(self, text: str) -> List[Tuple[str, int]]:
        """광고 스타일 자동 분류"""
        style_scores = {}

        for style, keywords in self.style_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                style_scores[style] = score

        # 점수 순으로 정렬
        sorted_styles = sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_styles if sorted_styles else [('기타', 0)]

    def classify_industry(self, text: str) -> List[Tuple[str, int]]:
        """산업군 자동 분류"""
        industry_scores = {}

        for industry, keywords in self.industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                industry_scores[industry] = score

        # 점수 순으로 정렬
        sorted_industries = sorted(industry_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_industries if sorted_industries else [('기타', 0)]

    def extract_keywords(self, words: List[str], top_n: int = 5) -> List[Tuple[str, int]]:
        """감성 키워드 추출"""
        keyword_scores = {}

        for word in words:
            if word in self.sentiment_dict and len(word) >= 2:
                score = abs(self.sentiment_dict[word])
                if score >= 1:  # 극성이 강한 단어만
                    keyword_scores[word] = self.sentiment_dict[word]

        # 극성 강도 순으로 정렬
        sorted_keywords = sorted(keyword_scores.items(), key=lambda x: abs(x[1]), reverse=True)
        return sorted_keywords[:top_n]

    def analyze_language_pattern(self, text: str) -> Dict:
        """언어 패턴 분석"""
        return {
            'length': len(text),
            'word_count': len(re.findall(r'[가-힣]+', text)),
            'has_question': '?' in text,
            'has_exclamation': '!' in text,
            'has_emoji': bool(re.search(r'[ㅋㅎ😀-🙏]+', text)),
            'sentence_count': len(re.split(r'[.!?]', text.strip()))
        }

    def detect_sentiment_conflict(self, positive_words: List[Tuple], negative_words: List[Tuple]) -> Dict:
        """감성 충돌 감지 및 분석"""
        pos_count = len(positive_words)
        neg_count = len(negative_words)

        # 긍정어/부정어 강도 합계
        pos_strength = sum(abs(score) for _, score in positive_words)
        neg_strength = sum(abs(score) for _, score in negative_words)

        has_conflict = pos_count >= 1 and neg_count >= 1

        conflict_type = None
        if has_conflict:
            # 양쪽 다 강하면 진짜 혼합
            if pos_count >= 2 and neg_count >= 2:
                conflict_type = "강한혼합"
            elif pos_strength > neg_strength * 1.5:
                conflict_type = "긍정우세혼합"
            elif neg_strength > pos_strength * 1.5:
                conflict_type = "부정우세혼합"
            else:
                conflict_type = "균형혼합"

        return {
            'has_conflict': has_conflict,
            'conflict_type': conflict_type,
            'positive_strength': pos_strength,
            'negative_strength': neg_strength
        }

    def analyze_text(self, text: str) -> Dict:
        """
        종합 텍스트 감성 분석
        """
        if not self.sentiment_dict:
            return None

        # 단어 추출
        words = self.extract_words(text)

        scores = []
        positive_words = []
        negative_words = []
        neutral_count = 0

        for word in words:
            if word in self.sentiment_dict:
                score = self.sentiment_dict[word]
                scores.append(score)

                if score >= 1:
                    positive_words.append((word, score))
                elif score <= -1:
                    negative_words.append((word, score))
                else:
                    neutral_count += 1

        # 평균 점수 계산
        avg_score = sum(scores) / len(scores) if scores else 0

        # 감성 충돌 감지
        conflict_info = self.detect_sentiment_conflict(positive_words, negative_words)

        # 감성 라벨 (혼합 감성 고려)
        if conflict_info['has_conflict']:
            conflict_type = conflict_info['conflict_type']

            if conflict_type == "강한혼합":
                label = "혼합(양립)"
            elif conflict_type == "긍정우세혼합":
                label = "혼합(긍정우세)"
            elif conflict_type == "부정우세혼합":
                label = "혼합(부정우세)"
            else:
                label = "혼합(균형)"
        else:
            # 기존 단일 감성 라벨
            if avg_score >= 1.5:
                label = "매우 긍정"
            elif avg_score >= 0.5:
                label = "긍정"
            elif avg_score <= -1.5:
                label = "매우 부정"
            elif avg_score <= -0.5:
                label = "부정"
            else:
                label = "중립"

        return {
            'score': round(avg_score, 2),
            'sentiment_label': label,
            'positive_words': positive_words,
            'negative_words': negative_words,
            'neutral_count': neutral_count,
            'total_sentiment_words': len(scores),
            'ad_styles': self.classify_ad_style(text),
            'industries': self.classify_industry(text),
            'keywords': self.extract_keywords(words),
            'language_pattern': self.analyze_language_pattern(text),
            'sentiment_conflict': conflict_info,
            'words': words[:10]  # 처음 10개 단어만 저장
        }


class AdPreferenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 AI 광고 취향 분석기 v4.0 GUI")
        self.root.geometry("1000x700")

        # 데이터 파일 경로 설정 (유연한 경로 탐색)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)

        # ad_data.json 경로 찾기: 1순위 현재 디렉토리, 2순위 ../script/
        data_paths = [
            os.path.join(script_dir, "ad_data.json"),
            os.path.join(parent_dir, "script", "ad_data.json")
        ]
        self.data_file = data_paths[0] if os.path.exists(data_paths[0]) else data_paths[1]

        # ad_copy_database.json 경로 찾기: 1순위 현재 디렉토리, 2순위 ../script/
        db_paths = [
            os.path.join(script_dir, "ad_copy_database.json"),
            os.path.join(parent_dir, "script", "ad_copy_database.json")
        ]
        self.ad_copy_db_file = db_paths[0] if os.path.exists(db_paths[0]) else db_paths[1]

        # 데이터 로드
        self.ads = self.load_data()
        self.ad_copy_database = self.load_ad_copy_database()

        # 감성 분석기 초기화
        print("🚀 AI 광고 취향 분석기 초기화 중...")
        self.sentiment_analyzer = AdvancedSentimentAnalyzer()

        # UI 구성
        self.setup_ui()

    def load_data(self):
        """저장된 데이터 불러오기"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def load_ad_copy_database(self):
        """광고 카피 데이터베이스 로드"""
        if os.path.exists(self.ad_copy_db_file):
            try:
                with open(self.ad_copy_db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ 광고 카피 DB 로드: {len(data)}개")
                return data
            except Exception as e:
                print(f"⚠️ 광고 카피 DB 로드 실패: {e}")
                return []
        else:
            print("⚠️ 광고 카피 데이터베이스를 찾을 수 없습니다.")
            return []

    def save_data(self):
        """데이터 저장하기"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.ads, f, ensure_ascii=False, indent=2)

    def setup_ui(self):
        """UI 구성"""
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')

        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 상단 정보 표시
        info_frame = ttk.LabelFrame(main_frame, text="📊 통계", padding="10")
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.stats_label = ttk.Label(info_frame, text=f"평가한 광고: {len(self.ads)}개", font=('Arial', 10, 'bold'))
        self.stats_label.pack()

        # 탭 컨트롤
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # 탭 생성
        self.create_rate_tab()
        self.create_analysis_tab()
        self.create_history_tab()
        self.create_recommend_tab()

        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 통계 업데이트
        self.update_stats()

    def create_rate_tab(self):
        """광고 평가 탭"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="📝 광고 평가하기")

        # 광고 입력
        ttk.Label(tab, text="광고 문구를 입력하세요:", font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)

        self.ad_text_input = scrolledtext.ScrolledText(tab, width=80, height=5, font=('Arial', 10))
        self.ad_text_input.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))

        # 분석 버튼
        analyze_btn = ttk.Button(tab, text="🤖 AI 분석하기", command=self.analyze_ad)
        analyze_btn.grid(row=2, column=0, pady=10)

        # 분석 결과 표시 영역
        result_frame = ttk.LabelFrame(tab, text="🔍 분석 결과", padding="10")
        result_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.analysis_result = scrolledtext.ScrolledText(result_frame, width=80, height=15, font=('Arial', 9))
        self.analysis_result.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 평가 입력 프레임
        rating_frame = ttk.LabelFrame(tab, text="⭐ 평가하기", padding="10")
        rating_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(rating_frame, text="이 광고가 마음에 드나요? (1-10):").grid(row=0, column=0, padx=5)
        self.rating_var = tk.IntVar(value=5)
        rating_scale = ttk.Scale(rating_frame, from_=1, to=10, variable=self.rating_var, orient=tk.HORIZONTAL, length=300)
        rating_scale.grid(row=0, column=1, padx=5)

        self.rating_label = ttk.Label(rating_frame, text="5", font=('Arial', 12, 'bold'))
        self.rating_label.grid(row=0, column=2, padx=5)

        # 스케일 값 변경 시 레이블 업데이트
        rating_scale.config(command=lambda v: self.rating_label.config(text=str(int(float(v)))))

        # 저장 버튼
        save_btn = ttk.Button(rating_frame, text="💾 평가 저장하기", command=self.save_rating)
        save_btn.grid(row=1, column=0, columnspan=3, pady=10)

        # 그리드 가중치
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

    def create_analysis_tab(self):
        """취향 분석 탭"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="🧠 AI 취향 분석")

        # 분석 버튼
        analyze_btn = ttk.Button(tab, text="🔄 취향 분석 새로고침", command=self.show_preference_analysis)
        analyze_btn.grid(row=0, column=0, pady=10)

        # 분석 결과 표시 영역
        self.analysis_text = scrolledtext.ScrolledText(tab, width=100, height=35, font=('Arial', 10))
        self.analysis_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 그리드 가중치
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

    def create_history_tab(self):
        """평가 기록 탭"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="📋 평가 기록")

        # 새로고침 버튼
        refresh_btn = ttk.Button(tab, text="🔄 기록 새로고침", command=self.show_history)
        refresh_btn.grid(row=0, column=0, pady=10)

        # 트리뷰로 기록 표시
        columns = ('No.', '광고 문구', '평점', '감성')
        self.history_tree = ttk.Treeview(tab, columns=columns, show='headings', height=25)

        self.history_tree.heading('No.', text='No.')
        self.history_tree.heading('광고 문구', text='광고 문구')
        self.history_tree.heading('평점', text='평점')
        self.history_tree.heading('감성', text='감성')

        self.history_tree.column('No.', width=50, anchor=tk.CENTER)
        self.history_tree.column('광고 문구', width=600, anchor=tk.W)
        self.history_tree.column('평점', width=80, anchor=tk.CENTER)
        self.history_tree.column('감성', width=120, anchor=tk.CENTER)

        self.history_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 스크롤바
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.history_tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        # 그리드 가중치
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

    def create_recommend_tab(self):
        """광고 카피 추천 탭"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="✨ 맞춤 광고 추천")

        # 추천 버튼
        recommend_btn = ttk.Button(tab, text="🎯 나에게 맞는 광고 카피 추천받기", command=self.show_recommendations)
        recommend_btn.grid(row=0, column=0, pady=10)

        # 추천 결과 표시 영역
        self.recommend_text = scrolledtext.ScrolledText(tab, width=100, height=35, font=('Arial', 10))
        self.recommend_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 그리드 가중치
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

    def analyze_ad(self):
        """광고 분석 실행"""
        ad_text = self.ad_text_input.get("1.0", tk.END).strip()

        if not ad_text:
            messagebox.showwarning("입력 오류", "광고 문구를 입력해주세요!")
            return

        # 분석 실행
        self.analysis_result.delete("1.0", tk.END)
        self.analysis_result.insert(tk.END, "🤖 AI 자동 분석 중...\n\n")
        self.root.update()

        sentiment_result = self.sentiment_analyzer.analyze_text(ad_text)

        if sentiment_result:
            # 분석 결과 표시
            result_text = self.format_analysis_result(sentiment_result)
            self.analysis_result.delete("1.0", tk.END)
            self.analysis_result.insert(tk.END, result_text)

            # 현재 분석 결과 저장 (나중에 평가 저장 시 사용)
            self.current_sentiment = sentiment_result
        else:
            self.analysis_result.delete("1.0", tk.END)
            self.analysis_result.insert(tk.END, "⚠️ 감성 분석을 수행할 수 없습니다.")

    def format_analysis_result(self, analysis: Dict) -> str:
        """분석 결과를 텍스트로 포맷팅"""
        result = "=" * 70 + "\n"
        result += "📊 AI 감성 분석 결과\n"
        result += "=" * 70 + "\n\n"

        # 감성 점수
        score = analysis['score']
        result += f"감성 라벨: [{analysis['sentiment_label']}]\n"
        result += f"감성 점수: {score}\n\n"

        # 주요 단어
        if analysis.get('words'):
            words_str = ', '.join(analysis['words'][:8])
            result += f"주요 단어: {words_str}\n\n"

        # 혼합 감성 정보
        if analysis.get('sentiment_conflict', {}).get('has_conflict'):
            conflict = analysis['sentiment_conflict']
            pos_words = [w[0] for w in analysis['positive_words'][:3]]
            neg_words = [w[0] for w in analysis['negative_words'][:3]]

            result += "⚡ 감성 충돌 감지!\n"
            result += f"  긍정어: {', '.join(pos_words)} (강도: {conflict['positive_strength']:.1f})\n"
            result += f"  부정어: {', '.join(neg_words)} (강도: {conflict['negative_strength']:.1f})\n\n"

            if conflict['conflict_type'] == "강한혼합":
                result += "  💡 스토리텔링형/역설형 광고로 추정됩니다\n\n"

        # 광고 스타일
        if analysis['ad_styles']:
            styles = ', '.join([f"{s[0]}({s[1]}점)" for s in analysis['ad_styles'][:3]])
            result += f"🎨 광고 스타일: {styles}\n\n"

        # 산업군
        if analysis.get('industries'):
            industries = ', '.join([f"{i[0]}({i[1]}점)" for i in analysis['industries'][:3]])
            result += f"🏢 산업군: {industries}\n\n"

        # 핵심 키워드
        if analysis['keywords']:
            keywords = ', '.join([f"'{k[0]}'({k[1]})" for k in analysis['keywords'][:5]])
            result += f"🔑 핵심 키워드: {keywords}\n\n"

        # 언어 패턴
        pattern = analysis['language_pattern']
        features = []
        if pattern['has_exclamation']:
            features.append("강조형")
        if pattern['has_question']:
            features.append("질문형")
        if pattern['length'] < 20:
            features.append("짧고 임팩트")
        elif pattern['length'] > 50:
            features.append("상세 설명형")

        if features:
            result += f"💬 표현 특징: {', '.join(features)}\n"

        result += "\n" + "=" * 70

        return result

    def save_rating(self):
        """평가 저장"""
        ad_text = self.ad_text_input.get("1.0", tk.END).strip()

        if not ad_text:
            messagebox.showwarning("입력 오류", "광고 문구를 입력해주세요!")
            return

        rating = self.rating_var.get()

        # 감성 분석 결과가 있는지 확인
        sentiment_result = getattr(self, 'current_sentiment', None)
        if not sentiment_result:
            # 분석이 안 되어 있으면 자동으로 분석
            sentiment_result = self.sentiment_analyzer.analyze_text(ad_text)

        # 데이터 저장
        ad_info = {
            "ad_text": ad_text,
            "overall_rating": rating,
            "sentiment_analysis": sentiment_result,
            "timestamp": datetime.now().isoformat()
        }

        self.ads.append(ad_info)
        self.save_data()

        # 통계 업데이트
        self.update_stats()

        # 성공 메시지
        messagebox.showinfo("저장 완료", f"✅ 광고 평가가 저장되었습니다!\n평점: {rating}/10")

        # 입력 초기화
        self.ad_text_input.delete("1.0", tk.END)
        self.analysis_result.delete("1.0", tk.END)
        self.rating_var.set(5)
        self.current_sentiment = None

    def update_stats(self):
        """통계 업데이트"""
        num_ads = len(self.ads)
        if num_ads > 0:
            avg_rating = sum(ad["overall_rating"] for ad in self.ads) / num_ads
            self.stats_label.config(text=f"평가한 광고: {num_ads}개 | 평균 만족도: {avg_rating:.1f}/10점")
        else:
            self.stats_label.config(text=f"평가한 광고: {num_ads}개")

    def show_preference_analysis(self):
        """취향 분석 표시"""
        self.analysis_text.delete("1.0", tk.END)

        if not self.ads:
            self.analysis_text.insert(tk.END, "아직 평가한 광고가 없습니다.\n광고를 평가하고 나만의 취향 프로필을 만들어보세요!")
            return

        result = "=" * 80 + "\n"
        result += "🧠 AI 기반 광고 취향 분석 리포트\n"
        result += "=" * 80 + "\n\n"

        num_ads = len(self.ads)
        avg_rating = sum(ad["overall_rating"] for ad in self.ads) / num_ads

        result += f"📈 평가 데이터: {num_ads}개 광고 | 평균 만족도: {avg_rating:.1f}/10점\n"
        result += "-" * 80 + "\n\n"

        # 감성 분석이 있는 광고만 추출
        ads_with_sentiment = [ad for ad in self.ads if ad.get("sentiment_analysis")]

        if ads_with_sentiment:
            # 감성 톤 선호도
            result += "🎭 감성 톤 선호도\n"
            result += "-" * 80 + "\n"

            sentiment_ratings = {}
            for ad in ads_with_sentiment:
                label = ad["sentiment_analysis"]["sentiment_label"]
                rating = ad["overall_rating"]

                if label not in sentiment_ratings:
                    sentiment_ratings[label] = []
                sentiment_ratings[label].append(rating)

            sorted_sentiments = sorted(
                sentiment_ratings.items(),
                key=lambda x: sum(x[1])/len(x[1]),
                reverse=True
            )

            for label, ratings in sorted_sentiments[:5]:
                avg = sum(ratings) / len(ratings)
                result += f"  {label:15s} | 평균: {avg:4.1f}점 | 평가 수: {len(ratings):3d}개\n"

            if sorted_sentiments:
                best_sentiment = sorted_sentiments[0][0]
                result += f"\n💡 당신은 '{best_sentiment}' 톤의 광고를 선호합니다.\n\n"

            # 광고 스타일 선호도
            result += "🎨 광고 스타일 선호도\n"
            result += "-" * 80 + "\n"

            style_ratings = {}
            for ad in ads_with_sentiment:
                if ad["sentiment_analysis"].get("ad_styles"):
                    main_style = ad["sentiment_analysis"]["ad_styles"][0][0]
                    rating = ad["overall_rating"]

                    if main_style not in style_ratings:
                        style_ratings[main_style] = []
                    style_ratings[main_style].append(rating)

            if style_ratings:
                sorted_styles = sorted(
                    style_ratings.items(),
                    key=lambda x: sum(x[1])/len(x[1]),
                    reverse=True
                )

                for style, ratings in sorted_styles[:5]:
                    avg = sum(ratings) / len(ratings)
                    result += f"  {style:15s} | 평균: {avg:4.1f}점 | 평가 수: {len(ratings):3d}개\n"

                best_style = sorted_styles[0][0]
                result += f"\n💡 당신은 '{best_style}' 광고를 가장 좋아합니다.\n\n"

        # 최고/최저 광고
        result += "⭐ 베스트 & 워스트\n"
        result += "-" * 80 + "\n"

        sorted_ads = sorted(self.ads, key=lambda x: x["overall_rating"], reverse=True)

        best_ad = sorted_ads[0]
        result += f"\n🏆 가장 마음에 든 광고 ({best_ad['overall_rating']}점):\n"
        result += f"   \"{best_ad['ad_text'][:100]}{'...' if len(best_ad['ad_text']) > 100 else ''}\"\n"

        if len(sorted_ads) >= 3:
            worst_ad = sorted_ads[-1]
            result += f"\n👎 아쉬웠던 광고 ({worst_ad['overall_rating']}점):\n"
            result += f"   \"{worst_ad['ad_text'][:100]}{'...' if len(worst_ad['ad_text']) > 100 else ''}\"\n"

        self.analysis_text.insert(tk.END, result)

    def show_history(self):
        """평가 기록 표시"""
        # 기존 항목 제거
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        if not self.ads:
            return

        # 데이터 추가
        for i, ad in enumerate(self.ads, 1):
            ad_text = ad['ad_text'][:60] + "..." if len(ad['ad_text']) > 60 else ad['ad_text']
            rating = f"{ad['overall_rating']}/10"

            sentiment = "N/A"
            if ad.get("sentiment_analysis"):
                sentiment = ad["sentiment_analysis"]["sentiment_label"]

            self.history_tree.insert('', tk.END, values=(i, ad_text, rating, sentiment))

    def show_recommendations(self):
        """맞춤 광고 추천 표시"""
        self.recommend_text.delete("1.0", tk.END)

        if not self.ad_copy_database:
            self.recommend_text.insert(tk.END, "광고 카피 데이터베이스가 비어있습니다.")
            return

        if len(self.ads) < 3:
            self.recommend_text.insert(tk.END, "추천을 위해서는 최소 3개 이상의 광고를 평가해주세요.")
            return

        self.recommend_text.insert(tk.END, "🤖 취향 분석 중...\n\n")
        self.root.update()

        recommendations = self.recommend_personalized_copies(top_n=10)

        if not recommendations:
            self.recommend_text.delete("1.0", tk.END)
            self.recommend_text.insert(tk.END, "추천할 수 있는 광고 카피를 찾을 수 없습니다.")
            return

        # 추천 결과 포맷팅
        result = "=" * 80 + "\n"
        result += "✨ AI 맞춤 광고 카피 추천\n"
        result += "=" * 80 + "\n\n"

        high_rated_count = len([ad for ad in self.ads if ad['overall_rating'] >= 7])
        result += f"📊 분석 기반: 높은 평가 광고 {high_rated_count}개\n"
        result += "-" * 80 + "\n\n"

        for idx, (copy_data, similarity, reason) in enumerate(recommendations, 1):
            result += f"{idx}. [{copy_data.get('category', 'N/A')}] {copy_data['text']}\n"
            result += f"   브랜드: {copy_data.get('brand', 'N/A')} | 유사도: {similarity:.2f}\n\n"

        # 카테고리 분포 분석
        category_count = {}
        for copy_data, _, _ in recommendations:
            category = copy_data.get('category', '기타')
            category_count[category] = category_count.get(category, 0) + 1

        if category_count:
            top_category = max(category_count.items(), key=lambda x: x[1])
            result += f"💡 당신은 '{top_category[0]}' 스타일 광고를 선호하시는 것 같아요! ({top_category[1]}개)\n\n"

        if len(category_count) > 1:
            result += f"카테고리 분포: {', '.join([f'{k}({v})' for k, v in sorted(category_count.items(), key=lambda x: x[1], reverse=True)])}\n"

        self.recommend_text.delete("1.0", tk.END)
        self.recommend_text.insert(tk.END, result)

    def recommend_personalized_copies(self, top_n: int = 10) -> List[Tuple[Dict, float, str]]:
        """사용자 취향 기반 광고 카피 추천"""
        if not self.ad_copy_database:
            return []

        if len(self.ads) < 3:
            return []

        # 높은 평가를 받은 광고 (7점 이상)
        high_rated_ads = [ad for ad in self.ads if ad['overall_rating'] >= 7]

        if not high_rated_ads:
            return []

        try:
            # 사용자가 좋아하는 광고 텍스트 수집
            user_liked_texts = [ad['ad_text'] for ad in high_rated_ads]

            # 광고 카피 DB 텍스트 수집
            db_texts = [copy['text'] for copy in self.ad_copy_database]

            # 모든 텍스트 합치기
            all_texts = user_liked_texts + db_texts

            # TF-IDF 벡터화
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(all_texts)

            # 사용자가 좋아하는 광고들의 평균 벡터 계산
            user_vectors = tfidf_matrix[:len(user_liked_texts)]
            user_profile = np.asarray(user_vectors.mean(axis=0))

            # DB 광고들과의 유사도 계산
            db_vectors = tfidf_matrix[len(user_liked_texts):]
            similarities = cosine_similarity(user_profile, db_vectors)[0]

            # 유사도가 0.1 이상인 것만 필터링
            valid_indices = [i for i, sim in enumerate(similarities) if sim >= 0.1]

            if not valid_indices:
                return []

            # 상위 N개 추천
            top_indices = sorted(valid_indices, key=lambda i: similarities[i], reverse=True)[:top_n]

            # 결과 구성
            recommendations = []
            for idx in top_indices:
                copy_data = self.ad_copy_database[idx]
                similarity = similarities[idx]
                reason = f"{copy_data.get('category', '기타')} 스타일"
                recommendations.append((copy_data, similarity, reason))

            return recommendations

        except Exception as e:
            print(f"⚠️ 추천 시스템 오류: {e}")
            return []


def main():
    root = tk.Tk()
    app = AdPreferenceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
