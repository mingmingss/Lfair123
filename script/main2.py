import json
import os
from datetime import datetime
from collections import Counter
import re
from typing import List, Dict, Tuple

# 새로운 라이브러리들
from kiwipiepy import Kiwi
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt
from rich import box

# Rich Console 초기화
console = Console()

class AdvancedSentimentAnalyzer:
    """KNU 한국어 감성사전 기반 고급 감성 분석기 (형태소 분석 강화)"""

    def __init__(self, senti_dict_path="SentiWord_info.json"):
        self.sentiment_dict = {}
        self.kiwi = Kiwi()
        self.load_sentiment_dict(senti_dict_path)

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

    def extract_morphemes(self, text: str) -> List[str]:
        """형태소 분석으로 의미있는 단어 추출"""
        result = self.kiwi.analyze(text)

        if not result:
            return []

        # 명사(NNG, NNP), 동사(VV), 형용사(VA), 영어(SL) 추출
        meaningful_pos = ['NNG', 'NNP', 'VV', 'VA', 'MAG', 'SL']
        morphemes = []

        for token in result[0][0]:
            if token.tag in meaningful_pos:
                morphemes.append(token.form)

        return morphemes

    def classify_ad_style(self, text: str, morphemes: List[str]) -> List[Tuple[str, int]]:
        """광고 스타일 자동 분류 (형태소 기반)"""
        style_scores = {}

        # 원본 텍스트와 형태소 모두에서 검색
        for style, keywords in self.style_keywords.items():
            score = 0
            for keyword in keywords:
                # 원본 텍스트에서 부분 문자열 검색
                if keyword in text:
                    score += 1
                # 형태소에서 정확히 일치하는 단어 검색
                elif keyword in morphemes:
                    score += 1

            if score > 0:
                style_scores[style] = score

        # 점수 순으로 정렬
        sorted_styles = sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_styles if sorted_styles else [('기타', 0)]

    def classify_industry(self, text: str, morphemes: List[str]) -> List[Tuple[str, int]]:
        """산업군 자동 분류 (형태소 기반)"""
        industry_scores = {}

        for industry, keywords in self.industry_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
                elif keyword in morphemes:
                    score += 1

            if score > 0:
                industry_scores[industry] = score

        # 점수 순으로 정렬
        sorted_industries = sorted(industry_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_industries if sorted_industries else [('기타', 0)]

    def extract_keywords(self, morphemes: List[str], top_n: int = 5) -> List[Tuple[str, int]]:
        """감성 키워드 추출 (형태소 기반)"""
        keyword_scores = {}

        for word in morphemes:
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
        종합 텍스트 감성 분석 (형태소 분석 적용)
        """
        if not self.sentiment_dict:
            return None

        # 형태소 분석
        morphemes = self.extract_morphemes(text)

        scores = []
        positive_words = []
        negative_words = []
        neutral_count = 0

        for word in morphemes:
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
            'ad_styles': self.classify_ad_style(text, morphemes),
            'industries': self.classify_industry(text, morphemes),
            'keywords': self.extract_keywords(morphemes),
            'language_pattern': self.analyze_language_pattern(text),
            'sentiment_conflict': conflict_info,
            'morphemes': morphemes[:10]  # 처음 10개 형태소만 저장
        }


class AdPreferenceAnalyzer:
    def __init__(self):
        self.data_file = "ad_data.json"
        self.ads = self.load_data()

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

    def save_data(self):
        """데이터 저장하기"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.ads, f, ensure_ascii=False, indent=2)

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

        # 평가 입력
        console.print(Panel.fit(
            "[bold yellow]⭐ 당신의 평가[/bold yellow]",
            border_style="yellow"
        ))
        overall_rating = IntPrompt.ask("\n[bold]이 광고가 마음에 드나요?[/bold]",
                                       default=5,
                                       show_default=True)

        while not (1 <= overall_rating <= 10):
            console.print("[red]1부터 10 사이의 점수를 입력하세요.[/red]")
            overall_rating = IntPrompt.ask("[bold]이 광고가 마음에 드나요?[/bold]", default=5)

        return {
            "ad_text": ad_text,
            "overall_rating": overall_rating,
            "sentiment_analysis": sentiment_result,
            "timestamp": datetime.now().isoformat()
        }

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
        if analysis.get('morphemes'):
            morphemes_str = ', '.join(analysis['morphemes'][:8])
            console.print(f"[dim]   형태소: {morphemes_str}...[/dim]")

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
                "[dim]powered by Kiwipiepy & Rich[/dim]",
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
            console.print("4. 종료")

            choice = IntPrompt.ask("\n[bold]선택[/bold]", choices=["1", "2", "3", "4"], default="1")

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
                console.print(Panel.fit(
                    "[bold green]프로그램을 종료합니다. 감사합니다! 👋[/bold green]",
                    border_style="green"
                ))
                break

if __name__ == "__main__":
    analyzer = AdPreferenceAnalyzer()
    analyzer.main_menu()
