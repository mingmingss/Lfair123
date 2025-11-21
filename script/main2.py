import json
import os
from datetime import datetime
from collections import Counter
import re
from typing import List, Dict, Tuple, Optional
import random

# UI 라이브러리
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt, Confirm
from rich import box

# 텍스트 유사도 분석 및 머신러닝
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Rich Console 초기화
console = Console()

class AdvancedSentimentAnalyzer:
    """KNU 한국어 감성사전 기반 감성 분석기"""

    def __init__(self, senti_dict_path="SentiWord_info.json"):
        self.sentiment_dict = {}

        # 현재 스크립트 디렉토리 기준으로 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, senti_dict_path)

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
            console.print(f"[yellow]⚠️  감성사전 파일({filepath})을 찾을 수 없습니다.[/yellow]")
            console.print("[yellow]감성 분석 기능이 비활성화됩니다.[/yellow]")
            return

        try:
            with console.status("[bold green]감성사전 로딩 중...", spinner="dots"):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 단어: 극성 매핑
                for item in data:
                    word = item['word']
                    polarity = int(item['polarity'])
                    self.sentiment_dict[word] = polarity

            console.print(f"[green]✅ 감성사전 로드 완료: {len(self.sentiment_dict):,}개 단어[/green]")
        except Exception as e:
            console.print(f"[red]⚠️  감성사전 로드 실패: {e}[/red]")

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


class AdPreferenceAnalyzer:
    def __init__(self):
        # 현재 스크립트 디렉토리 기준으로 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(script_dir, "ad_data.json")
        self.ads = self.load_data()

        # 광고 카피 데이터베이스 로드
        self.ad_copy_db_file = os.path.join(script_dir, "ad_copy_database.json")
        self.ad_copy_database = self.load_ad_copy_database()

        # 감성 분석기 초기화
        console.print("[bold cyan]🚀 AI 광고 취향 분석기 초기화 중...[/bold cyan]")
        self.sentiment_analyzer = AdvancedSentimentAnalyzer()

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
                console.print(f"[green]✅ 광고 카피 DB 로드: {len(data)}개[/green]")
                return data
            except Exception as e:
                console.print(f"[yellow]⚠️ 광고 카피 DB 로드 실패: {e}[/yellow]")
                return []
        else:
            console.print("[yellow]⚠️ 광고 카피 데이터베이스를 찾을 수 없습니다.[/yellow]")
            return []

    def save_data(self):
        """데이터 저장하기"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.ads, f, ensure_ascii=False, indent=2)

    def find_similar_ads(self, target_ad_text: str, top_n: int = 3) -> List[Tuple[Dict, float]]:
        """현재 광고와 유사한 광고 찾기 (TF-IDF + 코사인 유사도)"""
        if len(self.ads) < 2:
            return []

        try:
            # 모든 광고 텍스트 수집
            all_texts = [ad['ad_text'] for ad in self.ads]
            all_texts.append(target_ad_text)

            # TF-IDF 벡터화
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(all_texts)

            # 마지막 광고(target)와 다른 광고들의 유사도 계산
            similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]

            # 유사도가 0.1 이상인 광고만 필터링
            valid_indices = [i for i, sim in enumerate(similarities) if sim >= 0.1]

            if not valid_indices:
                return []

            # 가장 유사한 광고 인덱스 (내림차순)
            similar_indices = sorted(valid_indices, key=lambda i: similarities[i], reverse=True)[:top_n]

            return [(self.ads[i], similarities[i]) for i in similar_indices]

        except Exception as e:
            console.print(f"[yellow]⚠️ 유사도 분석 오류: {e}[/yellow]")
            return []

    def recommend_personalized_copies(self, top_n: int = 10) -> List[Tuple[Dict, float, str]]:
        """사용자 취향 기반 광고 카피 추천 (TF-IDF + 코사인 유사도)"""
        if not self.ad_copy_database:
            console.print("[yellow]광고 카피 데이터베이스가 비어있습니다.[/yellow]")
            return []

        if len(self.ads) < 3:
            console.print("[yellow]추천을 위해서는 최소 3개 이상의 광고를 평가해주세요.[/yellow]")
            return []

        # 높은 평가를 받은 광고 (7점 이상)
        high_rated_ads = [ad for ad in self.ads if ad['overall_rating'] >= 7]

        if not high_rated_ads:
            console.print("[yellow]7점 이상의 광고가 없습니다. 더 많은 광고를 평가해주세요.[/yellow]")
            return []

        try:
            # 사용자가 좋아하는 광고 텍스트 수집
            user_liked_texts = [ad['ad_text'] for ad in high_rated_ads]

            # 광고 카피 DB 텍스트 수집
            db_texts = [copy['text'] for copy in self.ad_copy_database]

            # 모든 텍스트 합치기 (사용자 선호 + DB)
            all_texts = user_liked_texts + db_texts

            # TF-IDF 벡터화
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(all_texts)

            # 사용자가 좋아하는 광고들의 평균 벡터 계산
            user_vectors = tfidf_matrix[:len(user_liked_texts)]
            user_profile = user_vectors.mean(axis=0)

            # DB 광고들과의 유사도 계산
            db_vectors = tfidf_matrix[len(user_liked_texts):]
            similarities = cosine_similarity(user_profile, db_vectors)[0]

            # 유사도가 0.1 이상인 것만 필터링
            valid_indices = [i for i, sim in enumerate(similarities) if sim >= 0.1]

            if not valid_indices:
                console.print("[yellow]유사한 광고 카피를 찾을 수 없습니다.[/yellow]")
                return []

            # 상위 N개 추천
            top_indices = sorted(valid_indices, key=lambda i: similarities[i], reverse=True)[:top_n]

            # 결과 구성: (광고 카피 dict, 유사도, 추천 이유)
            recommendations = []
            for idx in top_indices:
                copy_data = self.ad_copy_database[idx]
                similarity = similarities[idx]

                # 추천 이유 생성
                reason = f"{copy_data['category']} 스타일"

                recommendations.append((copy_data, similarity, reason))

            return recommendations

        except Exception as e:
            console.print(f"[red]⚠️ 추천 시스템 오류: {e}[/red]")
            return []

    def input_and_rate_ad(self):
        """광고 입력 및 평가 (Rich UI)"""
        console.print(Panel.fit(
            "[bold cyan]📝 광고 평가하기[/bold cyan]",
            border_style="cyan"
        ))

        # 광고 문구 입력
        ad_text = Prompt.ask("\n[bold]광고 문구를 입력하세요[/bold]").strip()
        while not ad_text:
            console.print("[red]광고 문구는 필수입니다![/red]")
            ad_text = Prompt.ask("[bold]광고 문구를 입력하세요[/bold]").strip()

        # AI 자동 분석
        console.print("\n" + "─"*70)
        with console.status("[bold green]🤖 AI 자동 분석 중...", spinner="dots"):
            sentiment_result = self.sentiment_analyzer.analyze_text(ad_text)
        console.print("─"*70)

        if sentiment_result:
            self.display_analysis_preview(sentiment_result)

        # 유사 광고 찾기 및 표시
        similar_ads = self.find_similar_ads(ad_text, top_n=3)
        if similar_ads:
            self.display_similar_ads(similar_ads)

        # 평가 입력
        console.print(Panel.fit(
            "[bold yellow]⭐ 당신의 평가[/bold yellow]",
            border_style="yellow"
        ))
        overall_rating = IntPrompt.ask("\n[bold]이 광고가 마음에 드나요? (1-10)[/bold]",
                                       default=5,
                                       show_default=True)

        while not (1 <= overall_rating <= 10):
            console.print("[red]1부터 10 사이의 점수를 입력하세요.[/red]")
            overall_rating = IntPrompt.ask("[bold]이 광고가 마음에 드나요? (1-10)[/bold]", default=5)

        return {
            "ad_text": ad_text,
            "overall_rating": overall_rating,
            "sentiment_analysis": sentiment_result,
            "timestamp": datetime.now().isoformat()
        }

    def display_similar_ads(self, similar_ads: List[Tuple[Dict, float]]):
        """유사 광고 표시"""
        console.print("\n[bold magenta]🔍 비슷한 광고를 찾았어요![/bold magenta]")

        # Rich Table 생성
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("광고 문구", style="white", width=40)
        table.add_column("유사도", justify="center", style="cyan", width=10)
        table.add_column("평점", justify="center", style="yellow", width=8)

        for ad, similarity in similar_ads:
            ad_text = ad['ad_text'][:37] + "..." if len(ad['ad_text']) > 40 else ad['ad_text']
            similarity_str = f"{similarity:.2f}"
            rating_str = f"{ad['overall_rating']}/10"
            table.add_row(ad_text, similarity_str, rating_str)

        console.print(table)

        # 평균 평점 계산 및 힌트 제공
        avg_similar_rating = sum(ad['overall_rating'] for ad, _ in similar_ads) / len(similar_ads)

        if avg_similar_rating >= 7:
            console.print(f"[green]💡 이전에 비슷한 광고를 높게 평가하셨네요! (평균 {avg_similar_rating:.1f}점)[/green]")
        elif avg_similar_rating <= 4:
            console.print(f"[yellow]💡 이전에 비슷한 광고를 낮게 평가하셨어요. (평균 {avg_similar_rating:.1f}점)[/yellow]")
        else:
            console.print(f"[dim]💡 비슷한 광고의 평균 평점: {avg_similar_rating:.1f}점[/dim]")

    def display_recommended_copies(self):
        """개인화 광고 카피 추천 표시"""
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]✨ AI 맞춤 광고 카피 추천[/bold cyan]\n"
            "[dim]당신의 취향을 분석해서 선별한 광고 카피들이에요[/dim]",
            border_style="cyan"
        ))

        # 추천 받기
        with console.status("[bold green]🤖 취향 분석 중...", spinner="dots"):
            recommendations = self.recommend_personalized_copies(top_n=10)

        if not recommendations:
            return

        # 사용자 통계 표시
        high_rated_count = len([ad for ad in self.ads if ad['overall_rating'] >= 7])
        console.print(f"\n[bold]📊 분석 기반:[/bold] 높은 평가 광고 {high_rated_count}개")
        console.print("─"*70)

        # Rich Table 생성
        table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
        table.add_column("순위", style="yellow", width=4, justify="center")
        table.add_column("광고 카피", style="white", width=40)
        table.add_column("브랜드", style="green", width=12)
        table.add_column("스타일", style="magenta", width=12)
        table.add_column("유사도", style="cyan", width=8, justify="center")

        for idx, (copy_data, similarity, reason) in enumerate(recommendations, 1):
            rank = str(idx)
            text = copy_data['text']
            brand = copy_data.get('brand', 'N/A')
            category = copy_data.get('category', 'N/A')
            sim_str = f"{similarity:.2f}"

            table.add_row(rank, text, brand, category, sim_str)

        console.print(table)

        # 카테고리 분포 분석
        category_count = {}
        for copy_data, _, _ in recommendations:
            category = copy_data.get('category', '기타')
            category_count[category] = category_count.get(category, 0) + 1

        # 가장 많은 카테고리
        if category_count:
            top_category = max(category_count.items(), key=lambda x: x[1])
            console.print(f"\n[bold green]💡 당신은 '{top_category[0]}' 스타일 광고를 선호하시는 것 같아요! ({top_category[1]}개)[/bold green]")

        # 카테고리 분포 표시
        if len(category_count) > 1:
            console.print(f"\n[dim]카테고리 분포: {', '.join([f'{k}({v})' for k, v in sorted(category_count.items(), key=lambda x: x[1], reverse=True)])}[/dim]")

    def display_analysis_preview(self, analysis: Dict):
        """분석 결과 미리보기 출력 (Rich 스타일)"""
        # 감성 점수에 따른 색상
        score = analysis['score']
        if score > 1:
            sentiment_color = "green"
        elif score > 0:
            sentiment_color = "cyan"
        elif score < -1:
            sentiment_color = "red"
        elif score < 0:
            sentiment_color = "yellow"
        else:
            sentiment_color = "white"

        console.print(f"\n[{sentiment_color}]📊 [{analysis['sentiment_label']}] (감성 점수: {score})[/{sentiment_color}]")

        # 형태소 분석 결과
        if analysis.get('words'):
            words_str = ', '.join(analysis['words'][:8])
            console.print(f"[dim]   주요 단어: {words_str}...[/dim]")

        # 혼합 감성 상세 정보
        if analysis.get('sentiment_conflict', {}).get('has_conflict'):
            conflict = analysis['sentiment_conflict']
            pos_words = [w[0] for w in analysis['positive_words'][:2]]
            neg_words = [w[0] for w in analysis['negative_words'][:2]]

            console.print(f"   [yellow]⚡ 감성 충돌 감지![/yellow]")
            console.print(f"      [green]긍정어: {', '.join(pos_words)} (강도: {conflict['positive_strength']:.1f})[/green]")
            console.print(f"      [red]부정어: {', '.join(neg_words)} (강도: {conflict['negative_strength']:.1f})[/red]")

            # 광고 유형 힌트
            if conflict['conflict_type'] == "강한혼합":
                console.print(f"      [cyan]💡 스토리텔링형/역설형 광고로 추정됩니다[/cyan]")

        # 광고 스타일
        if analysis['ad_styles']:
            styles = ', '.join([f"{s[0]}" for s in analysis['ad_styles'][:2]])
            console.print(f"[magenta]🎨 광고 스타일:[/magenta] {styles}")

        # 산업군
        if analysis.get('industries'):
            industries = ', '.join([f"{i[0]}" for i in analysis['industries'][:2]])
            console.print(f"[blue]🏢 산업군:[/blue] {industries}")

        # 핵심 키워드
        if analysis['keywords']:
            keywords = ', '.join([f"'{k[0]}'" for k in analysis['keywords'][:3]])
            console.print(f"[yellow]🔑 핵심 키워드:[/yellow] {keywords}")

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
            console.print(f"[cyan]💬 표현 특징:[/cyan] {', '.join(features)}")

    def add_new_ad(self):
        """새 광고 평가 전체 프로세스"""
        ad_info = self.input_and_rate_ad()

        # 데이터 저장
        self.ads.append(ad_info)
        self.save_data()

        console.print(Panel.fit(
            "[bold green]✅ 광고 평가가 완료되었습니다![/bold green]",
            border_style="green"
        ))

    def show_analysis(self):
        """스마트 취향 분석 (Rich 스타일)"""
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]🧠 AI 기반 광고 취향 분석 리포트[/bold cyan]",
            border_style="cyan"
        ))

        if not self.ads:
            console.print("\n[yellow]아직 평가한 광고가 없습니다.[/yellow]")
            console.print("[yellow]광고를 평가하고 나만의 취향 프로필을 만들어보세요![/yellow]")
            return

        num_ads = len(self.ads)
        avg_rating = sum(ad["overall_rating"] for ad in self.ads) / num_ads

        console.print(f"\n[bold]📈 평가 데이터:[/bold] {num_ads}개 광고 | [bold]평균 만족도:[/bold] {avg_rating:.1f}/10점")
        console.print("─"*70)

        # 감성 분석이 있는 광고만 추출
        ads_with_sentiment = [ad for ad in self.ads if ad.get("sentiment_analysis")]

        if ads_with_sentiment:
            self.show_sentiment_preference(ads_with_sentiment)
            self.show_style_preference(ads_with_sentiment)

        self.show_top_and_bottom_ads()

    def show_sentiment_preference(self, ads: List[Dict]):
        """감성 톤 선호도 분석 (테이블 스타일)"""
        console.print("\n[bold magenta]🎭 감성 톤 선호도[/bold magenta]")

        # 감성 라벨별 평균 점수
        sentiment_ratings = {}

        for ad in ads:
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

        # Rich Table 생성
        table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
        table.add_column("감성 톤", style="cyan", width=15)
        table.add_column("평균 점수", justify="right", style="yellow")
        table.add_column("평가 수", justify="right", style="dim")

        for label, ratings in sorted_sentiments[:5]:
            avg = sum(ratings) / len(ratings)
            table.add_row(label, f"{avg:.1f}점", f"{len(ratings)}개")

        console.print(table)

        if sorted_sentiments:
            best_sentiment = sorted_sentiments[0][0]
            console.print(f"\n[bold green]💡 당신은 '{best_sentiment}' 톤의 광고를 선호합니다.[/bold green]")

    def show_style_preference(self, ads: List[Dict]):
        """광고 스타일 선호도 분석"""
        console.print("\n[bold blue]🎨 광고 스타일 선호도[/bold blue]")

        style_ratings = {}
        for ad in ads:
            if ad["sentiment_analysis"].get("ad_styles"):
                # 첫 번째 스타일만 (주 스타일)
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

            # Rich Table 생성
            table = Table(show_header=True, header_style="bold blue", box=box.ROUNDED)
            table.add_column("광고 스타일", style="blue", width=15)
            table.add_column("평균 점수", justify="right", style="yellow")
            table.add_column("평가 수", justify="right", style="dim")

            for style, ratings in sorted_styles[:5]:
                avg = sum(ratings) / len(ratings)
                table.add_row(style, f"{avg:.1f}점", f"{len(ratings)}개")

            console.print(table)

            best_style = sorted_styles[0][0]
            console.print(f"\n[bold green]💡 당신은 '{best_style}' 광고를 가장 좋아합니다.[/bold green]")

    def show_top_and_bottom_ads(self):
        """최고/최저 광고"""
        console.print("\n[bold yellow]⭐ 베스트 & 워스트[/bold yellow]")
        console.print("─"*70)

        sorted_ads = sorted(self.ads, key=lambda x: x["overall_rating"], reverse=True)

        # 최고 광고
        best_ad = sorted_ads[0]
        console.print(f"\n[green]🏆 가장 마음에 든 광고 ({best_ad['overall_rating']}점):[/green]")
        console.print(f"   [bold]\"{best_ad['ad_text'][:50]}{'...' if len(best_ad['ad_text']) > 50 else ''}\"[/bold]")

        # 최저 광고
        if len(sorted_ads) >= 3:
            worst_ad = sorted_ads[-1]
            console.print(f"\n[red]👎 아쉬웠던 광고 ({worst_ad['overall_rating']}점):[/red]")
            console.print(f"   [dim]\"{worst_ad['ad_text'][:50]}{'...' if len(worst_ad['ad_text']) > 50 else ''}\"[/dim]")

    def show_history(self):
        """평가 기록 보기 (테이블 스타일)"""
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]📋 평가 기록[/bold cyan]",
            border_style="cyan"
        ))

        if not self.ads:
            console.print("\n[yellow]아직 평가한 광고가 없습니다.[/yellow]")
            return

        # Rich Table 생성
        table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
        table.add_column("No.", style="dim", width=4)
        table.add_column("광고 문구", style="white", width=40)
        table.add_column("평점", justify="center", style="yellow", width=6)
        table.add_column("감성", justify="center", style="cyan", width=12)

        for i, ad in enumerate(self.ads, 1):
            ad_text = ad['ad_text'][:37] + "..." if len(ad['ad_text']) > 40 else ad['ad_text']
            rating = f"{ad['overall_rating']}/10"

            # 감성 분석 결과
            sentiment = "N/A"
            if ad.get("sentiment_analysis"):
                sentiment = ad["sentiment_analysis"]["sentiment_label"]

            table.add_row(str(i), ad_text, rating, sentiment)

        console.print(table)

    def main_menu(self):
        """메인 메뉴 (Rich 스타일)"""
        while True:
            console.clear()
            console.print(Panel.fit(
                "[bold cyan]🎯 AI 광고 취향 분석기 v4.0[/bold cyan]\n"
                "[dim]powered by TF-IDF & Rich[/dim]",
                border_style="cyan"
            ))

            console.print(f"\n[bold]📊 현재까지 평가한 광고:[/bold] [yellow]{len(self.ads)}개[/yellow]")

            if len(self.ads) >= 3:
                avg_rating = sum(ad["overall_rating"] for ad in self.ads) / len(self.ads)
                console.print(f"[bold]⭐ 평균 만족도:[/bold] [yellow]{avg_rating:.1f}/10점[/yellow]")

            console.print("\n[bold cyan][메뉴][/bold cyan]")
            console.print("1. 광고 평가하기")
            console.print("2. AI 취향 분석 보기")
            console.print("3. 평가 기록 보기")
            console.print("4. ✨ 맞춤 광고 카피 추천 받기")
            console.print("5. 종료")

            choice = IntPrompt.ask("\n[bold]선택[/bold]", choices=["1", "2", "3", "4", "5"], default="1")

            if choice == 1:
                self.add_new_ad()
                Prompt.ask("\n[dim]계속하려면 Enter를 누르세요[/dim]", default="")
            elif choice == 2:
                self.show_analysis()
                Prompt.ask("\n[dim]계속하려면 Enter를 누르세요[/dim]", default="")
            elif choice == 3:
                self.show_history()
                Prompt.ask("\n[dim]계속하려면 Enter를 누르세요[/dim]", default="")
            elif choice == 4:
                self.display_recommended_copies()
                Prompt.ask("\n[dim]계속하려면 Enter를 누르세요[/dim]", default="")
            elif choice == 5:
                console.print(Panel.fit(
                    "[bold green]프로그램을 종료합니다. 감사합니다! 👋[/bold green]",
                    border_style="green"
                ))
                break

if __name__ == "__main__":
    analyzer = AdPreferenceAnalyzer()
    analyzer.main_menu()
