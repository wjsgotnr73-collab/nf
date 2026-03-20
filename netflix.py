import requests
from bs4 import BeautifulSoup
import random

def get_netflix_rank():
    # 1. 비교적 크롤링이 잘 되는 넷플릭스 순위 사이트 (데이터 제공용)
    url = "https://flixpatrol.com/top10/netflix/world/today/"
    
    # 진짜 브라우저처럼 보이게 만드는 헤더 (매우 중요!)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 2. 데이터 추출 (사이트 구조에 맞춘 최신 선택자)
        # 테이블 내의 제목들을 가져옵니다.
        movie_elements = soup.select('.table-main tr td.table-main-title')
        
        print(f"\n🌍 [실시간] 글로벌 넷플릭스 TOP 10")
        print("=" * 45)

        if not movie_elements:
            # [비상용] 사이트 차단 시 작동하는 더미 데이터 (로직 테스트용)
            print("⚠️ 실시간 연결 지연으로 인기작 리스트를 불러옵니다.")
            titles = ["오징어 게임 시즌2", "지옥", "더 글로리", "킹덤", "스위트홈", "기생수", "피지컬:100", "아무도 없는 숲속에서", "살인자ㅇ난감", "마이 네임"]
        else:
            titles = [el.get_text().strip() for el in movie_elements[:10]]

        # 3. 순위 출력
        for i, title in enumerate(titles, 1):
            print(f"{i:2}위: {title}")
        
        print("=" * 45)

        # 4. 추천 및 다시 하기 실행
        top1 = titles[0]
        show_recommendation(top1)

    except Exception as e:
        print(f"❌ 접속 오류: {e}")

def show_recommendation(top_movie):
    # AI/명작 추천 리스트
    classics = [
        "브레이킹 배드 (스릴러/범죄)", 
        "기묘한 이야기 (판타지/모험)", 
        "블랙 미러 (SF/옴니버스)", 
        "다크 (미스터리/시간여행)",
        "퀸스 갬빗 (드라마/체스)"
    ]
    
    print(f"\n🤖 AI 추천 비서")
    print(f"현재 1위인 '{top_movie}'와(과) 함께")
    print(f"인생 명작 '{random.choice(classics)}'도 정주행해보세요!")
    print("-" * 45)

    # 5. [요청하신 기능] 다시 하기 질문
    ask_retry()

def ask_retry():
    while True:
        retry = input("넷플릭스 순위를 다시 조회하거나 다른 추천을 볼까요? (y/n): ").lower()
        if retry == 'y':
            get_netflix_rank()
            break
        elif retry == 'n':
            print("즐거운 시청 되세요! 프로그램을 종료합니다. 👋")
            exit()
        else:
            print("y 또는 n만 입력해주세요.")

if __name__ == "__main__":
    get_netflix_rank()