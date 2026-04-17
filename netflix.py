import requests
import re

def pharmacy_search_fixed():
    # 님의 인증키 (그대로 유지)
    service_key = "90577787f9dd0e6155ce016bc0d88bd3709a15b0206b98b3c5201119599ebdd4"
    
    while True:
        print("\n" + "="*55)
        print("🏥 실시간 약국 검색 (주소 오류 수정 버전)")
        print("="*55)

        city = input("📍 시/도 (예: 서울특별시): ").strip()
        district = input("📍 구/군 (예: 강남구): ").strip()

        if not city or not district:
            continue

        # [수정됨] API 엔드포인트 주소를 더 정확한 경로로 변경했습니다.
        url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getPharmacyListInfoInqire'
        
        params = {
            'serviceKey' : service_key,
            'Q0' : city,
            'Q1' : district,
            'pageNo' : '1',
            'numOfRows' : '10'
        }

        try:
            print(f"📡 '{city} {district}' 조회 중...")
            response = requests.get(url, params=params, timeout=10)
            
            # 디버깅용 (문제가 생기면 내용을 보기 위함)
            content = response.text

            if "API not found" in content:
                print("❌ 여전히 주소 오류가 발생합니다. 다른 경로로 재시도합니다...")
                # 백업 경로로 한 번 더 시도
                url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getPharmacyLcinfoInqire'
                response = requests.get(url, params=params, timeout=10)
                content = response.text

            # 데이터 쪼개기
            items = content.split('<item>')
            items = items[1:]

            if not items:
                print("❌ 검색 결과가 없습니다.")
                print("메시지:", content) # 서버가 보내는 에러 메시지 직접 확인
            else:
                print(f"\n🔍 검색 결과 ({len(items)}곳):")
                print("-" * 60)
                for item in items:
                    def extract(tag, xml):
                        match = re.search(f'<{tag}>(.*?)</{tag}>', xml)
                        return match.group(1) if match else "정보없음"
                    
                    name = extract('dutyName', item)
                    tel = extract('dutyTel1', item)
                    addr = extract('dutyAddr', item)
                    
                    print(f"▶ {name}\n   📞 {tel}\n   🏠 {addr}")
                    print("-" * 60)

        except Exception as e:
            print(f"❌ 접속 오류: {e}")

        print("\n더 알아보시겠습니까? (Y/N)")
        if input(">> ").strip().upper() != 'Y':
            print("👋 종료합니다!")
            break

if __name__ == "__main__":
    pharmacy_search_fixed()