import json
import os
from datetime import datetime
from collections import Counter
import re
from typing import List, Dict, Tuple

class AdvancedSentimentAnalyzer:
    """KNU 한국어 감성사전 기반 고급 감성 분석기"""

    def __init__(self, senti_dict_path="SentiWord_info.json"):
        self.sentiment_dict = {}
        self.load_sentiment_dict(senti_dict_path)

        # 광고 스타일 키워드 사전 (확장)
        self.style_keywords = {
            '유머형': ['ㅋ', 'ㅎ', '웃', '재미', '유머', '우습', '깔깔', '하하'],
            '감성형': ['마음', '사랑', '행복', '따뜻', '소중', '감동', '추억', '함께', '가족', '일상', '순간'],
            '정보형': ['새로운', '최초', '기술', '혁신', '특허', '개발', '성분', '효과', '과학'],
            '긴급형': ['지금', '오늘', '한정', '마지막', '서둘', '빨리', '곧', '즉시', '바로'],
            '프리미엄형': ['프리미엄', '럭셔리', '고급', '명품', '최고급', '특별', '한정판', '격'],
            '실용형': ['편리', '간편', '실용', '유용', '효율', '절약', '알뜰', '가성비', '쉽', '빠른'],
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
            
            print(f"✅ 감성사전 로드 완료: {len(self.sentiment_dict)}개 단어")
        except Exception as e:
            print(f"⚠️  감성사전 로드 실패: {e}")
    
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

    def extract_keywords(self, text: str, top_n: int = 5) -> List[Tuple[str, int]]:
        """감성 키워드 추출 (감성사전 기반)"""
        words = re.findall(r'[가-힣]+', text)
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
        Returns: {
            'score': 감성 점수,
            'sentiment_label': 감성 라벨,
            'positive_words': 긍정어 리스트,
            'negative_words': 부정어 리스트,
            'ad_styles': 광고 스타일 분류,
            'keywords': 핵심 키워드,
            'language_pattern': 언어 패턴 분석,
            'sentiment_conflict': 감성 충돌 정보
        }
        """
        if not self.sentiment_dict:
            return None

        # 단어 추출
        words = re.findall(r'[가-힣]+|[a-zA-Z]+', text)

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
            'keywords': self.extract_keywords(text),
            'language_pattern': self.analyze_language_pattern(text),
            'sentiment_conflict': conflict_info
        }


class AdPreferenceAnalyzer:
    def __init__(self):
        self.data_file = "ad_data.json"
        self.ads = self.load_data()

        # 감성 분석기 초기화
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
    
    def clear_screen(self):
        """화면 클리어 (선택적)"""
        print("\n" + "="*60 + "\n")
    
    def show_numbered_list(self, items, title):
        """번호 목록 출력"""
        print(f"\n{title}")
        for i, item in enumerate(items, 1):
            print(f"{i}) {item}")
    
    def get_choice(self, prompt, max_num):
        """번호 선택 입력 받기"""
        while True:
            try:
                choice = int(input(f"{prompt} (1-{max_num}): "))
                if 1 <= choice <= max_num:
                    return choice
                print(f"1부터 {max_num} 사이의 숫자를 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")
    
    def get_rating(self, prompt, min_val=1, max_val=10):
        """점수 입력 받기"""
        while True:
            try:
                rating = int(input(f"{prompt} ({min_val}-{max_val}점): "))
                if min_val <= rating <= max_val:
                    return rating
                print(f"{min_val}부터 {max_val} 사이의 점수를 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")
    
    def input_and_rate_ad(self):
        """광고 입력 및 평가 (간소화 버전)"""
        print("\n" + "="*70)
        print("📝 광고 평가하기")
        print("="*70)

        # 광고 문구 입력
        ad_text = input("\n광고 문구를 입력하세요: ").strip()
        while not ad_text:
            print("광고 문구는 필수입니다!")
            ad_text = input("광고 문구를 입력하세요: ").strip()

        # AI 자동 분석
        print("\n" + "─"*70)
        print("🤖 AI 자동 분석 중...")
        print("─"*70)
        sentiment_result = self.sentiment_analyzer.analyze_text(ad_text)

        if sentiment_result:
            self.display_analysis_preview(sentiment_result)

        # 간단한 평가
        print("\n" + "="*70)
        print("⭐ 당신의 평가")
        print("="*70)
        overall_rating = self.get_rating("\n이 광고가 마음에 드나요?", 1, 10)

        return {
            "ad_text": ad_text,
            "overall_rating": overall_rating,
            "sentiment_analysis": sentiment_result,
            "timestamp": datetime.now().isoformat()
        }

    def batch_input_ads(self):
        """여러 광고 한 번에 입력"""
        print("\n" + "="*70)
        print("📝 배치 평가 - 광고 입력")
        print("="*70)
        print("\n여러 광고를 한 번에 입력하세요.")
        print("각 광고는 한 줄씩 입력하고, 빈 줄을 입력하면 종료됩니다.")
        print("또는 'q'를 입력하면 종료됩니다.")
        print("\n예시:")
        print("  1번째 광고: 당신의 행복을 위한 선택")
        print("  2번째 광고: 지금 바로 시작하세요!")
        print("  3번째 광고: (Enter - 입력 종료)")
        print("─"*70)

        ads = []
        line_num = 1

        while True:
            ad_text = input(f"\n{line_num}번째 광고 (빈 줄 또는 'q' 입력시 종료): ").strip()

            if not ad_text or ad_text.lower() == 'q':
                break

            ads.append(ad_text)
            line_num += 1

        return ads

    def rate_single_ad(self, ad_text: str, index: int, total: int):
        """단일 광고 평가 (배치용)"""
        print("\n" + "="*70)
        print(f"📝 광고 평가 [{index}/{total}]")
        print("="*70)
        print(f"\n광고: \"{ad_text}\"")

        # AI 자동 분석
        print("\n" + "─"*70)
        print("🤖 AI 자동 분석 중...")
        print("─"*70)
        sentiment_result = self.sentiment_analyzer.analyze_text(ad_text)

        if sentiment_result:
            self.display_analysis_preview(sentiment_result)

        # 간단한 평가
        print("\n" + "="*70)
        print("⭐ 당신의 평가")
        print("="*70)
        overall_rating = self.get_rating("\n이 광고가 마음에 드나요?", 1, 10)

        return {
            "ad_text": ad_text,
            "overall_rating": overall_rating,
            "sentiment_analysis": sentiment_result,
            "timestamp": datetime.now().isoformat()
        }

    def batch_evaluate_ads(self):
        """배치 평가 전체 프로세스"""
        # 1단계: 광고들 입력
        ads = self.batch_input_ads()

        if not ads:
            print("\n입력된 광고가 없습니다.")
            return

        print(f"\n✅ 총 {len(ads)}개의 광고가 입력되었습니다.")
        print("이제 차례대로 평가를 진행합니다.\n")
        input("준비되면 Enter를 누르세요...")

        # 2단계: 각 광고 순차 평가
        evaluated_ads = []
        for i, ad_text in enumerate(ads, 1):
            ad_info = self.rate_single_ad(ad_text, i, len(ads))
            evaluated_ads.append(ad_info)

            # 마지막이 아니면 다음으로
            if i < len(ads):
                print("\n" + "─"*70)
                input("다음 광고로 넘어가려면 Enter를 누르세요...")

        # 3단계: 모두 저장
        self.ads.extend(evaluated_ads)
        self.save_data()

        # 4단계: 요약 표시
        print("\n" + "="*70)
        print("🎉 배치 평가 완료!")
        print("="*70)
        print(f"\n총 {len(evaluated_ads)}개 광고 평가 완료")

        avg_rating = sum(ad["overall_rating"] for ad in evaluated_ads) / len(evaluated_ads)
        print(f"평균 만족도: {avg_rating:.1f}/10점")

        # 최고/최저 광고
        sorted_batch = sorted(evaluated_ads, key=lambda x: x["overall_rating"], reverse=True)
        best = sorted_batch[0]
        worst = sorted_batch[-1]

        print(f"\n🏆 이번 배치 최고 광고 ({best['overall_rating']}점):")
        print(f"   \"{best['ad_text'][:50]}{'...' if len(best['ad_text']) > 50 else ''}\"")

        if len(evaluated_ads) >= 3:
            print(f"\n👎 이번 배치 최저 광고 ({worst['overall_rating']}점):")
            print(f"   \"{worst['ad_text'][:50]}{'...' if len(worst['ad_text']) > 50 else ''}\"")

        print("\n" + "="*70)

    def display_analysis_preview(self, analysis: Dict):
        """분석 결과 미리보기 출력"""
        print(f"\n📊 [{analysis['sentiment_label']}] (감성 점수: {analysis['score']})")

        # 혼합 감성 상세 정보
        if analysis.get('sentiment_conflict', {}).get('has_conflict'):
            conflict = analysis['sentiment_conflict']
            pos_words = [w[0] for w in analysis['positive_words'][:2]]
            neg_words = [w[0] for w in analysis['negative_words'][:2]]

            print(f"   ⚡ 감성 충돌 감지!")
            print(f"      긍정어: {', '.join(pos_words)} (강도: {conflict['positive_strength']:.1f})")
            print(f"      부정어: {', '.join(neg_words)} (강도: {conflict['negative_strength']:.1f})")

            # 광고 유형 힌트
            if conflict['conflict_type'] == "강한혼합":
                print(f"      💡 스토리텔링형/역설형 광고로 추정됩니다")

        # 광고 스타일
        if analysis['ad_styles']:
            styles = ', '.join([f"{s[0]}" for s in analysis['ad_styles'][:2]])
            print(f"🎨 광고 스타일: {styles}")

        # 산업군
        if analysis.get('industries'):
            industries = ', '.join([f"{i[0]}" for i in analysis['industries'][:2]])
            print(f"🏢 산업군: {industries}")

        # 핵심 키워드
        if analysis['keywords']:
            keywords = ', '.join([f"'{k[0]}'" for k in analysis['keywords'][:3]])
            print(f"🔑 핵심 키워드: {keywords}")

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
            print(f"💬 표현 특징: {', '.join(features)}")
    
    def add_new_ad(self):
        """새 광고 평가 전체 프로세스"""
        ad_info = self.input_and_rate_ad()

        # 데이터 저장
        self.ads.append(ad_info)
        self.save_data()

        print("\n" + "="*70)
        print("✅ 광고 평가가 완료되었습니다!")
        print("="*70)
    
    def show_analysis(self):
        """스마트 취향 분석"""
        self.clear_screen()
        print("="*70)
        print("🧠 AI 기반 광고 취향 분석 리포트")
        print("="*70)

        if not self.ads:
            print("\n아직 평가한 광고가 없습니다.")
            print("광고를 평가하고 나만의 취향 프로필을 만들어보세요!")
            return

        num_ads = len(self.ads)
        avg_rating = sum(ad["overall_rating"] for ad in self.ads) / num_ads

        print(f"\n📈 평가 데이터: {num_ads}개 광고 | 평균 만족도: {avg_rating:.1f}/10점")
        print("─"*70)

        # 감성 분석이 있는 광고만 추출
        ads_with_sentiment = [ad for ad in self.ads if ad.get("sentiment_analysis")]

        if ads_with_sentiment:
            self.show_sentiment_preference(ads_with_sentiment)
            self.show_style_preference(ads_with_sentiment)
            self.show_language_preference(ads_with_sentiment)

            if num_ads >= 5:
                self.show_advanced_insights(ads_with_sentiment)

        self.show_top_and_bottom_ads()

    def show_sentiment_preference(self, ads: List[Dict]):
        """감성 톤 선호도 분석"""
        print("\n🎭 감성 톤 선호도")
        print("─"*70)

        # 감성 라벨별 평균 점수
        sentiment_ratings = {}
        mixed_sentiment_ads = []

        for ad in ads:
            label = ad["sentiment_analysis"]["sentiment_label"]
            rating = ad["overall_rating"]

            if label not in sentiment_ratings:
                sentiment_ratings[label] = []
            sentiment_ratings[label].append(rating)

            # 혼합 감성 광고 별도 추적
            if "혼합" in label:
                mixed_sentiment_ads.append(ad)

        sorted_sentiments = sorted(
            sentiment_ratings.items(),
            key=lambda x: sum(x[1])/len(x[1]),
            reverse=True
        )

        for label, ratings in sorted_sentiments[:3]:
            avg = sum(ratings) / len(ratings)
            print(f"  • {label} 톤: {avg:.1f}점 평균 ({len(ratings)}개)")

        # 가장 선호하는 감성 톤
        if sorted_sentiments:
            best_sentiment = sorted_sentiments[0][0]
            print(f"\n💡 당신은 '{best_sentiment}' 톤의 광고를 선호합니다.")

        # 혼합 감성 광고 분석
        if mixed_sentiment_ads:
            mixed_avg = sum(ad["overall_rating"] for ad in mixed_sentiment_ads) / len(mixed_sentiment_ads)
            print(f"\n⚡ 혼합 감성 광고: {mixed_avg:.1f}점 평균 ({len(mixed_sentiment_ads)}개)")

            if mixed_avg >= 7:
                print(f"   → 복잡한 감정을 담은 스토리텔링 광고를 즐깁니다!")
            elif mixed_avg < 5:
                print(f"   → 명확한 메시지를 선호하는 편입니다.")

    def show_style_preference(self, ads: List[Dict]):
        """광고 스타일 선호도 분석"""
        print("\n🎨 광고 스타일 선호도")
        print("─"*70)

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

            for style, ratings in sorted_styles[:3]:
                avg = sum(ratings) / len(ratings)
                print(f"  • {style}: {avg:.1f}점 평균 ({len(ratings)}개)")

            best_style = sorted_styles[0][0]
            print(f"\n💡 당신은 '{best_style}' 광고를 가장 좋아합니다.")

    def show_language_preference(self, ads: List[Dict]):
        """언어 패턴 선호도 분석"""
        print("\n💬 언어 패턴 선호도")
        print("─"*70)

        # language_pattern이 있는 광고만 필터링
        ads_with_pattern = [ad for ad in ads if ad["sentiment_analysis"].get("language_pattern")]

        if not ads_with_pattern:
            print("  (언어 패턴 데이터 없음)")
            return

        # 길이별 선호도
        short_ads = [ad for ad in ads_with_pattern if ad["sentiment_analysis"]["language_pattern"]["length"] < 20]
        long_ads = [ad for ad in ads_with_pattern if ad["sentiment_analysis"]["language_pattern"]["length"] > 50]

        if short_ads:
            short_avg = sum(ad["overall_rating"] for ad in short_ads) / len(short_ads)
            print(f"  • 짧은 광고 (20자 미만): {short_avg:.1f}점 ({len(short_ads)}개)")

        if long_ads:
            long_avg = sum(ad["overall_rating"] for ad in long_ads) / len(long_ads)
            print(f"  • 긴 광고 (50자 이상): {long_avg:.1f}점 ({len(long_ads)}개)")

        # 강조형/질문형 선호도
        exclamation_ads = [ad for ad in ads_with_pattern if ad["sentiment_analysis"]["language_pattern"]["has_exclamation"]]
        question_ads = [ad for ad in ads_with_pattern if ad["sentiment_analysis"]["language_pattern"]["has_question"]]

        if exclamation_ads:
            exc_avg = sum(ad["overall_rating"] for ad in exclamation_ads) / len(exclamation_ads)
            print(f"  • 강조형 (!) 광고: {exc_avg:.1f}점 ({len(exclamation_ads)}개)")

        if question_ads:
            q_avg = sum(ad["overall_rating"] for ad in question_ads) / len(question_ads)
            print(f"  • 질문형 (?) 광고: {q_avg:.1f}점 ({len(question_ads)}개)")

    def show_advanced_insights(self, ads: List[Dict]):
        """고급 인사이트 (5개 이상일 때)"""
        print("\n🎯 AI 인사이트")
        print("─"*70)

        # 효과적인 키워드 찾기
        keyword_ratings = {}
        for ad in ads:
            keywords = ad["sentiment_analysis"].get("keywords", [])
            rating = ad["overall_rating"]

            for keyword, _ in keywords[:2]:  # 상위 2개 키워드만
                if keyword not in keyword_ratings:
                    keyword_ratings[keyword] = []
                keyword_ratings[keyword].append(rating)

        # 키워드가 2번 이상 등장한 것만
        frequent_keywords = {k: v for k, v in keyword_ratings.items() if len(v) >= 2}

        if frequent_keywords:
            sorted_keywords = sorted(
                frequent_keywords.items(),
                key=lambda x: sum(x[1])/len(x[1]),
                reverse=True
            )

            print("  당신에게 효과적인 단어들:")
            for keyword, ratings in sorted_keywords[:3]:
                avg = sum(ratings) / len(ratings)
                print(f"    • '{keyword}' → {avg:.1f}점 평균")

        # 감성-만족도 상관관계
        self.analyze_sentiment_score_correlation(ads)

    def analyze_sentiment_score_correlation(self, ads: List[Dict]):
        """감성 점수와 만족도의 상관관계"""
        positive_ads = [ad for ad in ads if ad["sentiment_analysis"]["score"] > 0.5]
        negative_ads = [ad for ad in ads if ad["sentiment_analysis"]["score"] < -0.5]

        if len(positive_ads) >= 2 and len(negative_ads) >= 2:
            pos_avg = sum(ad["overall_rating"] for ad in positive_ads) / len(positive_ads)
            neg_avg = sum(ad["overall_rating"] for ad in negative_ads) / len(negative_ads)

            print(f"\n  감성 톤에 따른 만족도:")
            print(f"    • 긍정적 표현: {pos_avg:.1f}점")
            print(f"    • 부정적 표현: {neg_avg:.1f}점")

            if pos_avg > neg_avg + 1:
                print(f"    → 당신은 밝고 긍정적인 광고를 선호합니다!")
            elif neg_avg > pos_avg + 0.5:
                print(f"    → 솔직하고 현실적인 광고가 더 와닿습니다!")

    def show_top_and_bottom_ads(self):
        """최고/최저 광고"""
        print("\n⭐ 베스트 & 워스트")
        print("─"*70)

        sorted_ads = sorted(self.ads, key=lambda x: x["overall_rating"], reverse=True)

        # 최고 광고
        best_ad = sorted_ads[0]
        print(f"\n🏆 가장 마음에 든 광고 ({best_ad['overall_rating']}점):")
        print(f"   \"{best_ad['ad_text'][:50]}{'...' if len(best_ad['ad_text']) > 50 else ''}\"")

        # 최저 광고
        if len(sorted_ads) >= 3:
            worst_ad = sorted_ads[-1]
            print(f"\n👎 아쉬웠던 광고 ({worst_ad['overall_rating']}점):")
            print(f"   \"{worst_ad['ad_text'][:50]}{'...' if len(worst_ad['ad_text']) > 50 else ''}\")")
    
    
    def show_history(self):
        """평가 기록 보기"""
        self.clear_screen()
        print("="*70)
        print("📋 평가 기록")
        print("="*70)

        if not self.ads:
            print("\n아직 평가한 광고가 없습니다.")
            return

        for i, ad in enumerate(self.ads, 1):
            print(f"\n[{i}] {ad['ad_text']}")
            print(f"    만족도: {ad['overall_rating']}/10점")

            # 감성 분석 결과 표시
            if ad.get("sentiment_analysis"):
                sent = ad["sentiment_analysis"]
                print(f"    감성 톤: {sent['sentiment_label']} (점수: {sent['score']})")

                if sent.get('ad_styles'):
                    styles = ', '.join([s[0] for s in sent['ad_styles'][:2]])
                    print(f"    스타일: {styles}")

            date_str = datetime.fromisoformat(ad['timestamp']).strftime("%Y-%m-%d %H:%M")
            print(f"    평가 시간: {date_str}")
    
    def main_menu(self):
        """메인 메뉴"""
        while True:
            self.clear_screen()
            print("="*70)
            print("🎯 AI 광고 취향 분석기 v3.1")
            print("="*70)
            print(f"\n📊 현재까지 평가한 광고: {len(self.ads)}개")

            if len(self.ads) >= 3:
                avg_rating = sum(ad["overall_rating"] for ad in self.ads) / len(self.ads)
                print(f"⭐ 평균 만족도: {avg_rating:.1f}/10점")

            print("\n[메뉴]")
            print("1. 광고 평가하기 (1개)")
            print("2. 배치 평가하기 (여러 개)")
            print("3. AI 취향 분석 보기")
            print("4. 평가 기록 보기")
            print("5. 종료")

            choice = self.get_choice("\n선택", 5)

            if choice == 1:
                self.add_new_ad()
                input("\n계속하려면 Enter를 누르세요...")
            elif choice == 2:
                self.batch_evaluate_ads()
                input("\n계속하려면 Enter를 누르세요...")
            elif choice == 3:
                self.show_analysis()
                input("\n계속하려면 Enter를 누르세요...")
            elif choice == 4:
                self.show_history()
                input("\n계속하려면 Enter를 누르세요...")
            elif choice == 5:
                print("\n" + "="*70)
                print("프로그램을 종료합니다. 감사합니다! 👋")
                print("="*70)
                break

if __name__ == "__main__":
    analyzer = AdPreferenceAnalyzer()
    analyzer.main_menu()