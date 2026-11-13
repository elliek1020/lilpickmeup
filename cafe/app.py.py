import random
import urllib.parse
import streamlit as st

st.set_page_config(page_title="대신 골라드려요 - 카페 메뉴 정하기", layout="centered")

# 1. 카드형 버튼 & 코지 카페 컬러 팔레트 스타일
st.markdown("""
    <style>
        /* 좌측 기본 멀티페이지 파일 목록 숨기기 */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        /* 전체 배경: 크림 아이보리 */
        .stApp {
            background-color: #EFE9DE;
            color: #2E1B11;
        }
        /* 사이드바: 따뜻한 베이지 */
        [data-testid="stSidebar"] {
            background-color: #E5DDD0;
            border-right: 1px solid #CFC3B0;
        }
        /* 메인 타이틀 & 서브타이틀 */
        .main-title {
            text-align: center;
            color: #A62626;
            font-size: 2.3rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 2px;
        }
        .sub-title {
            text-align: center;
            color: #2E1B11;
            font-size: 1.15rem;
            font-weight: 600;
            margin-top: 0;
            margin-bottom: 20px;
        }

        /* 시작 CTA 버튼 ('오늘은 뭘 마실까?') */
        div.element-container:has(.green-cta) + div.element-container button {
            background-color: #3B4D2B !important;
            color: #F6F1E7 !important;
            border: 1px solid #2C3A20 !important;
            border-bottom: 3px solid #222D18 !important;
            padding: 15px 20px !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            box-shadow: 0 3px 8px rgba(46, 27, 17, 0.16) !important;
            transition: all 0.15s ease !important;
        }
        div.element-container:has(.green-cta) + div.element-container button:hover {
            background-color: #2F3E22 !important;
            transform: translateY(1px);
        }

        /* [문답 선택 카드] 기본(미선택) 상태 */
        div.element-container:has(.choice-box) + div.element-container button[kind="secondary"] {
            width: 100% !important;
            min-height: 112px !important;
            background-color: #FAF7F2 !important;
            color: #2E1B11 !important;
            border: 1.5px solid #D8CBB8 !important;
            border-radius: 14px !important;
            padding: 18px 14px !important;
            white-space: pre-line !important;
            line-height: 1.55 !important;
            box-shadow: 0 2px 6px rgba(46, 27, 17, 0.04) !important;
            transition: all 0.15s ease !important;
        }
        div.element-container:has(.choice-box) + div.element-container button[kind="secondary"]:hover {
            border-color: #3B4D2B !important;
            background-color: #F5F7F2 !important;
            transform: translateY(-2px);
        }

        /* [문답 선택 카드] 선택된 상태 -> 두꺼운 초록색 외곽선 */
        div.element-container:has(.choice-box) + div.element-container button[kind="primary"] {
            width: 100% !important;
            min-height: 112px !important;
            background-color: #EEF3E9 !important;
            color: #2E1B11 !important;
            border: 3.5px solid #3B4D2B !important;
            border-radius: 14px !important;
            padding: 18px 14px !important;
            white-space: pre-line !important;
            line-height: 1.55 !important;
            box-shadow: 0 4px 12px rgba(59, 77, 43, 0.18) !important;
            transition: all 0.15s ease !important;
        }
        div.element-container:has(.choice-box) + div.element-container button p {
            font-size: 0.95rem !important;
            margin: 0 !important;
            color: #2E1B11 !important;
        }

        /* 최종 추천 메뉴 확인 버튼 */
        div.element-container:has(.submit-btn) + div.element-container button {
            background-color: #A62626 !important;
            border: 1px solid #871D1D !important;
            border-bottom: 3px solid #6E1616 !important;
            color: #F6F1E7 !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            padding: 12px !important;
        }
        div.element-container:has(.submit-btn) + div.element-container button:hover {
            background-color: #8C1F1F !important;
            border-color: #701717 !important;
        }

        /* 추천 결과 음료 일러스트 카드 */
        .drink-hero-box {
            background-color: #FAF7F2;
            border: 2px solid #A62626;
            border-radius: 18px;
            padding: 26px 20px;
            text-align: center;
            margin: 14px 0;
            box-shadow: 0 6px 18px rgba(46, 27, 17, 0.08);
        }

        /* 바이럴 & 커스텀 레시피 카드 */
        .recipe-card {
            background-color: #FAF7F2;
            border: 1.5px solid #D8CBB8;
            border-left: 5px solid #3B4D2B;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# 2. 서울 지하철역 목록 (충무로역이 기본값)
SEOUL_STATIONS = [
    "충무로역", "을지로3가역", "을지로입구역", "시청역", "종각역", "광화문역",
    "서울역", "명동역", "동대문역사문화공원역", "강남역", "역삼역", "선릉역",
    "삼성역", "교대역", "서초역", "신논현역", "여의도역", "국회의사당역",
    "영등포구청역", "오목교역", "목동역", "당산역", "공덕역", "마포역",
    "홍대입구역", "합정역", "신촌역", "성수역", "건대입구역", "왕십리역",
    "잠실역", "종합운동장역", "구로디지털단지역", "가산디지털단지역", "사당역"
]

STATION_CAFES = {
    "충무로역": [
        {"brand": "스타벅스", "branch": "충무로역점 (4번 출구 도보 1분)"},
        {"brand": "메가MGC커피", "branch": "충무로역점 (5번 출구 도보 1분)"},
        {"brand": "컴포즈커피", "branch": "충무로역점 (1번 출구 도보 2분)"},
        {"brand": "투썸플레이스", "branch": "충무로역점 (3번 출구 도보 2분)"},
        {"brand": "매머드커피", "branch": "충무로점 (6번 출구 도보 3분)"},
    ],
    "을지로3가역": [
        {"brand": "스타벅스", "branch": "을지로3가역점 (1번 출구 도보 1분)"},
        {"brand": "메가MGC커피", "branch": "을지로3가역점 (도보 1분)"},
        {"brand": "매머드커피", "branch": "을지로3가점 (도보 2분)"},
        {"brand": "컴포즈커피", "branch": "을지로3가점 (도보 2분)"},
    ],
    "오목교역": [
        {"brand": "스타벅스", "branch": "오목교역점 (1번 출구 도보 1분)"},
        {"brand": "투썸플레이스", "branch": "오목교역점 (도보 2분)"},
        {"brand": "메가MGC커피", "branch": "오목교역점 (도보 2분)"},
        {"brand": "컴포즈커피", "branch": "오목교역점 (도보 3분)"},
    ],
    "강남역": [
        {"brand": "스타벅스", "branch": "강남R점 (11번 출구 도보 2분)"},
        {"brand": "메가MGC커피", "branch": "강남역점 (도보 1분)"},
        {"brand": "컴포즈커피", "branch": "강남역점 (도보 2분)"},
        {"brand": "매머드커피", "branch": "강남대로점 (도보 2분)"},
    ],
    "여의도역": [
        {"brand": "스타벅스", "branch": "여의도역점 (5번 출구 도보 1분)"},
        {"brand": "매머드커피", "branch": "여의도점 (도보 2분)"},
        {"brand": "컴포즈커피", "branch": "여의도역점 (도보 2분)"},
        {"brand": "투썸플레이스", "branch": "여의도역점 (도보 3분)"},
    ]
}

# 3. 브랜드별 음료 + 일러스트 + 영양성분 데이터
DRINKS = [
    # [스타벅스]
    {"brand": "스타벅스", "name": "아이스 아메리카노 (블론드)", "caffeine": True, "temp": "ICE", "sweet": False, "milk": False, "illust": "iced_americano",
     "nutrition": {"kcal": 10, "caffeine": 170, "sugar": 0, "protein": 1, "fat": 0}},
    {"brand": "스타벅스", "name": "따뜻한 아메리카노", "caffeine": True, "temp": "HOT", "sweet": False, "milk": False, "illust": "hot_americano",
     "nutrition": {"kcal": 10, "caffeine": 150, "sugar": 0, "protein": 1, "fat": 0}},
    {"brand": "스타벅스", "name": "아이스 카페 라떼", "caffeine": True, "temp": "ICE", "sweet": False, "milk": True, "illust": "iced_latte",
     "nutrition": {"kcal": 110, "caffeine": 75, "sugar": 8, "protein": 6, "fat": 4}},
    {"brand": "스타벅스", "name": "따뜻한 플랫 화이트", "caffeine": True, "temp": "HOT", "sweet": False, "milk": True, "illust": "hot_latte",
     "nutrition": {"kcal": 170, "caffeine": 130, "sugar": 13, "protein": 9, "fat": 6}},
    {"brand": "스타벅스", "name": "아이스 돌체 콜드 브루", "caffeine": True, "temp": "ICE", "sweet": True, "milk": True, "illust": "cream_latte",
     "nutrition": {"kcal": 265, "caffeine": 155, "sugar": 29, "protein": 8, "fat": 9}},
    {"brand": "스타벅스", "name": "따뜻한 화이트 초콜릿 모카", "caffeine": True, "temp": "HOT", "sweet": True, "milk": True, "illust": "hot_latte",
     "nutrition": {"kcal": 345, "caffeine": 75, "sugar": 42, "protein": 11, "fat": 13}},
    {"brand": "스타벅스", "name": "아이스 자몽 허니 블랙 티", "caffeine": True, "temp": "ICE", "sweet": True, "milk": False, "illust": "fruit_ade",
     "nutrition": {"kcal": 125, "caffeine": 30, "sugar": 30, "protein": 0, "fat": 0}},
    {"brand": "스타벅스", "name": "아이스 유자 민트 티", "caffeine": False, "temp": "ICE", "sweet": True, "milk": False, "illust": "fruit_ade",
     "nutrition": {"kcal": 145, "caffeine": 0, "sugar": 34, "protein": 0, "fat": 0}},
    {"brand": "스타벅스", "name": "시그니처 핫 초콜릿", "caffeine": False, "temp": "HOT", "sweet": True, "milk": True, "illust": "hot_latte",
     "nutrition": {"kcal": 330, "caffeine": 15, "sugar": 36, "protein": 12, "fat": 12}},
    {"brand": "스타벅스", "name": "따뜻한 캐모마일 블렌드 티", "caffeine": False, "temp": "HOT", "sweet": False, "milk": False, "illust": "hot_tea",
     "nutrition": {"kcal": 0, "caffeine": 0, "sugar": 0, "protein": 0, "fat": 0}},

    # [메가MGC커피]
    {"brand": "메가MGC커피", "name": "아이스 아메리카노", "caffeine": True, "temp": "ICE", "sweet": False, "milk": False, "illust": "iced_americano",
     "nutrition": {"kcal": 12, "caffeine": 193, "sugar": 0, "protein": 1, "fat": 0}},
    {"brand": "메가MGC커피", "name": "할메가커피", "caffeine": True, "temp": "ICE", "sweet": True, "milk": True, "illust": "cream_latte",
     "nutrition": {"kcal": 286, "caffeine": 195, "sugar": 34, "protein": 5, "fat": 10}},
    {"brand": "메가MGC커피", "name": "큐브라떼", "caffeine": True, "temp": "ICE", "sweet": False, "milk": True, "illust": "iced_latte",
     "nutrition": {"kcal": 195, "caffeine": 210, "sugar": 14, "protein": 8, "fat": 8}},
    {"brand": "메가MGC커피", "name": "따뜻한 바닐라 라떼", "caffeine": True, "temp": "HOT", "sweet": True, "milk": True, "illust": "hot_latte",
     "nutrition": {"kcal": 295, "caffeine": 185, "sugar": 32, "protein": 8, "fat": 9}},
    {"brand": "메가MGC커피", "name": "복숭아 아이스티 (샷 추가)", "caffeine": True, "temp": "ICE", "sweet": True, "milk": False, "illust": "fruit_ade",
     "nutrition": {"kcal": 165, "caffeine": 98, "sugar": 38, "protein": 0, "fat": 0}},
    {"brand": "메가MGC커피", "name": "딸기라떼", "caffeine": False, "temp": "ICE", "sweet": True, "milk": True, "illust": "cream_latte",
     "nutrition": {"kcal": 340, "caffeine": 0, "sugar": 46, "protein": 7, "fat": 8}},
    {"brand": "메가MGC커피", "name": "따뜻한 사과유자차", "caffeine": False, "temp": "HOT", "sweet": True, "milk": False, "illust": "hot_tea",
     "nutrition": {"kcal": 210, "caffeine": 0, "sugar": 49, "protein": 0, "fat": 0}},
    {"brand": "메가MGC커피", "name": "아이스 페퍼민트 티", "caffeine": False, "temp": "ICE", "sweet": False, "milk": False, "illust": "fruit_ade",
     "nutrition": {"kcal": 4, "caffeine": 0, "sugar": 0, "protein": 0, "fat": 0}},

    # [컴포즈커피]
    {"brand": "컴포즈커피", "name": "아이스 아메리카노", "caffeine": True, "temp": "ICE", "sweet": False, "milk": False, "illust": "iced_americano",
     "nutrition": {"kcal": 15, "caffeine": 156, "sugar": 0, "protein": 1, "fat": 0}},
    {"brand": "컴포즈커피", "name": "아인슈페너 라떼", "caffeine": True, "temp": "ICE", "sweet": True, "milk": True, "illust": "cream_latte",
     "nutrition": {"kcal": 310, "caffeine": 156, "sugar": 26, "protein": 7, "fat": 15}},
    {"brand": "컴포즈커피", "name": "따뜻한 카페라떼", "caffeine": True, "temp": "HOT", "sweet": False, "milk": True, "illust": "hot_latte",
     "nutrition": {"kcal": 180, "caffeine": 156, "sugar": 13, "protein": 9, "fat": 9}},
    {"brand": "컴포즈커피", "name": "자몽에이드", "caffeine": False, "temp": "ICE", "sweet": True, "milk": False, "illust": "fruit_ade",
     "nutrition": {"kcal": 190, "caffeine": 0, "sugar": 45, "protein": 0, "fat": 0}},
    {"brand": "컴포즈커피", "name": "팥절미 밀크쉐이크", "caffeine": False, "temp": "ICE", "sweet": True, "milk": True, "illust": "shake",
     "nutrition": {"kcal": 495, "caffeine": 0, "sugar": 62, "protein": 11, "fat": 14}},

    # [투썸플레이스]
    {"brand": "투썸플레이스", "name": "아이스 아메리카노 (블랙그라운드)", "caffeine": True, "temp": "ICE", "sweet": False, "milk": False, "illust": "iced_americano",
     "nutrition": {"kcal": 15, "caffeine": 145, "sugar": 0, "protein": 1, "fat": 0}},
    {"brand": "투썸플레이스", "name": "스페니쉬 연유 라떼", "caffeine": True, "temp": "ICE", "sweet": True, "milk": True, "illust": "cream_latte",
     "nutrition": {"kcal": 290, "caffeine": 145, "sugar": 33, "protein": 8, "fat": 10}},
    {"brand": "투썸플레이스", "name": "로얄 밀크티 쉐이크", "caffeine": True, "temp": "ICE", "sweet": True, "milk": True, "illust": "shake",
     "nutrition": {"kcal": 460, "caffeine": 65, "sugar": 54, "protein": 8, "fat": 16}},
    {"brand": "투썸플레이스", "name": "TWG 1837 블랙티", "caffeine": True, "temp": "HOT", "sweet": False, "milk": False, "illust": "hot_tea",
     "nutrition": {"kcal": 5, "caffeine": 40, "sugar": 0, "protein": 0, "fat": 0}},
    {"brand": "투썸플레이스", "name": "스트로베리 피치 프라페", "caffeine": False, "temp": "ICE", "sweet": True, "milk": False, "illust": "shake",
     "nutrition": {"kcal": 285, "caffeine": 0, "sugar": 61, "protein": 1, "fat": 0}},

    # [매머드커피]
    {"brand": "매머드커피", "name": "아이스 아메리카노", "caffeine": True, "temp": "ICE", "sweet": False, "milk": False, "illust": "iced_americano",
     "nutrition": {"kcal": 14, "caffeine": 210, "sugar": 0, "protein": 1, "fat": 0}},
    {"brand": "매머드커피", "name": "꿀 라떼", "caffeine": True, "temp": "ICE", "sweet": True, "milk": True, "illust": "iced_latte",
     "nutrition": {"kcal": 255, "caffeine": 205, "sugar": 29, "protein": 8, "fat": 8}},
    {"brand": "매머드커피", "name": "아몬드 아메리카노", "caffeine": True, "temp": "ICE", "sweet": True, "milk": False, "illust": "iced_americano",
     "nutrition": {"kcal": 95, "caffeine": 210, "sugar": 18, "protein": 1, "fat": 1}},
    {"brand": "매머드커피", "name": "수박 주스", "caffeine": False, "temp": "ICE", "sweet": True, "milk": False, "illust": "fruit_ade",
     "nutrition": {"kcal": 180, "caffeine": 0, "sugar": 41, "protein": 1, "fat": 0}},
]

# 4. 결과 음료 전용 일러스트 SVG
def get_drink_illustration(illust_type):
    illustrations = {
        "iced_americano": '''
            <svg width="110" height="110" viewBox="0 0 120 120">
                <line x1="72" y1="10" x2="62" y2="40" stroke="#3B4D2B" stroke-width="5" stroke-linecap="round"/>
                <polygon points="35,38 85,38 78,105 42,105" fill="#3B2316" stroke="#2E1B11" stroke-width="3"/>
                <rect x="44" y="46" width="14" height="14" rx="3" fill="#D8E8EC" opacity="0.85"/>
                <rect x="62" y="52" width="13" height="13" rx="3" fill="#D8E8EC" opacity="0.85"/>
                <ellipse cx="60" cy="38" rx="26" ry="5" fill="#FAF7F2" stroke="#2E1B11" stroke-width="2.5"/>
            </svg>''',
        "hot_americano": '''
            <svg width="110" height="110" viewBox="0 0 120 120">
                <path d="M45 26 Q40 16 48 10" fill="none" stroke="#C85219" stroke-width="3" stroke-linecap="round"/>
                <path d="M60 24 Q55 14 63 8" fill="none" stroke="#C85219" stroke-width="3" stroke-linecap="round"/>
                <path d="M75 26 Q70 16 78 10" fill="none" stroke="#C85219" stroke-width="3" stroke-linecap="round"/>
                <polygon points="36,42 84,42 77,104 43,104" fill="#EFE9DE" stroke="#2E1B11" stroke-width="3"/>
                <polygon points="38,58 82,58 80,82 40,82" fill="#A62626"/>
                <rect x="33" y="35" width="54" height="8" rx="3" fill="#2E1B11"/>
            </svg>''',
        "iced_latte": '''
            <svg width="110" height="110" viewBox="0 0 120 120">
                <line x1="70" y1="10" x2="60" y2="40" stroke="#A62626" stroke-width="5" stroke-linecap="round"/>
                <polygon points="35,38 85,38 78,105 42,105" fill="#EADBC8" stroke="#2E1B11" stroke-width="3"/>
                <polygon points="36,42 84,42 81,72 39,72" fill="#8C583A"/>
                <rect x="46" y="45" width="13" height="13" rx="3" fill="#FAF7F2" opacity="0.75"/>
                <ellipse cx="60" cy="38" rx="26" ry="5" fill="#FAF7F2" stroke="#2E1B11" stroke-width="2.5"/>
            </svg>''',
        "hot_latte": '''
            <svg width="110" height="110" viewBox="0 0 120 120">
                <path d="M30,52 H82 V76 A26,26 0 0,1 30,76 Z" fill="#B57B50" stroke="#2E1B11" stroke-width="3"/>
                <path d="M82,58 H92 A8,8 0 0,1 92,74 H82" fill="none" stroke="#2E1B11" stroke-width="3"/>
                <ellipse cx="56" cy="52" rx="26" ry="7" fill="#FAF7F2" stroke="#2E1B11" stroke-width="2.5"/>
                <path d="M56,55 C50,49 46,53 56,59 C66,53 62,49 56,55 Z" fill="#A62626"/>
                <ellipse cx="56" cy="103" rx="34" ry="5" fill="#D8CBB8" stroke="#2E1B11" stroke-width="2.5"/>
            </svg>''',
        "cream_latte": '''
            <svg width="110" height="110" viewBox="0 0 120 120">
                <polygon points="35,44 85,44 78,105 42,105" fill="#6F442B" stroke="#2E1B11" stroke-width="3"/>
                <path d="M34,44 Q45,24 60,26 Q75,24 86,44 Z" fill="#FAF7F2" stroke="#2E1B11" stroke-width="2.5"/>
                <circle cx="60" cy="24" r="4" fill="#A62626"/>
            </svg>''',
        "fruit_ade": '''
            <svg width="110" height="110" viewBox="0 0 120 120">
                <line x1="74" y1="10" x2="62" y2="40" stroke="#3B4D2B" stroke-width="5" stroke-linecap="round"/>
                <polygon points="35,38 85,38 78,105 42,105" fill="#D96B43" stroke="#2E1B11" stroke-width="3"/>
                <circle cx="52" cy="65" r="9" fill="#A62626" opacity="0.85"/>
                <circle cx="66" cy="82" r="4" fill="#FAF7F2" opacity="0.85"/>
                <circle cx="50" cy="88" r="3" fill="#FAF7F2" opacity="0.85"/>
                <ellipse cx="60" cy="38" rx="26" ry="5" fill="#FAF7F2" stroke="#2E1B11" stroke-width="2.5"/>
            </svg>''',
        "hot_tea": '''
            <svg width="110" height="110" viewBox="0 0 120 120">
                <path d="M32,50 H80 V78 A24,24 0 0,1 32,78 Z" fill="#DFB15B" stroke="#2E1B11" stroke-width="3"/>
                <path d="M80,56 H90 A8,8 0 0,1 90,72 H80" fill="none" stroke="#2E1B11" stroke-width="3"/>
                <line x1="68" y1="50" x2="94" y2="74" stroke="#2E1B11" stroke-width="2"/>
                <rect x="88" y="70" width="12" height="14" rx="2" fill="#3B4D2B"/>
            </svg>''',
        "shake": '''
            <svg width="110" height="110" viewBox="0 0 120 120">
                <line x1="60" y1="8" x2="60" y2="38" stroke="#A62626" stroke-width="6" stroke-linecap="round"/>
                <path d="M35,44 A25,22 0 0,1 85,44 Z" fill="#FAF7F2" stroke="#2E1B11" stroke-width="2.5"/>
                <polygon points="35,44 85,44 78,105 42,105" fill="#E3C7A6" stroke="#2E1B11" stroke-width="3"/>
                <circle cx="52" cy="62" r="5" fill="#5C3A21"/>
                <circle cx="67" cy="70" r="5" fill="#5C3A21"/>
            </svg>'''
    }
    return illustrations.get(illust_type, illustrations["iced_americano"])

# 5. 세션 상태 초기화
defaults = {
    "started": False,
    "caffeine": True,
    "temp": "ICE",
    "sweet": False,
    "milk": False,
    "station": "충무로역",
    "result_drink": None,
    "selected_branch_str": ""
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# 6. 좌측 사이드바 메뉴
with st.sidebar:
    st.markdown("<h3 style='color: #A62626; font-weight: 800; margin-bottom: 2px;'>대신 골라드려요</h3>", unsafe_allow_html=True)
    st.caption("직장인 점심시간 음료 큐레이션")
    st.divider()
    
    menu_page = st.radio(
        "메뉴 이동",
        ["카페 메뉴 정하기", "요즘 바이럴 메뉴", "꿀조합 커스텀 레시피"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown(
        "<div style='background-color: #FAF7F2; border: 1px solid #D8CBB8; padding: 12px; border-radius: 10px; font-size: 0.82rem; color: #2E1B11;'>"
        "<b>참고 팁</b><br>점심 식사 직후에는 아메리카노보다 15분 뒤 차(Tea)나 연한 라떼가 철분 흡수를 덜 방해합니다."
        "</div>",
        unsafe_allow_html=True
    )

# ==============================================================================
# [페이지 1] 카페 메뉴 정하기 (메인)
# ==============================================================================
if menu_page == "카페 메뉴 정하기":
    st.markdown("<div class='main-title'>대신 골라드려요</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>카페 메뉴 정하기</div>", unsafe_allow_html=True)

    st.markdown('<div class="green-cta"></div>', unsafe_allow_html=True)
    if st.button("오늘은 뭘 마실까?", use_container_width=True):
        st.session_state.started = True

    if st.session_state.started:
        st.divider()

        # [수정된 부분] '[선택됨]' 문구 제거 + 선택된 카드에 두꺼운 초록색 외곽선 적용
        def render_clickable_card_choice(title, state_key, opt1, opt2):
            st.markdown(f"#### {title}")
            c1, c2 = st.columns(2)
            
            with c1:
                is_active = (st.session_state[state_key] == opt1["val"])
                card_text = f"**{opt1['label']}**\n\n{opt1['sub']}"
                st.markdown('<div class="choice-box"></div>', unsafe_allow_html=True)
                if st.button(
                    card_text,
                    key=f"{state_key}_1",
                    type="primary" if is_active else "secondary",
                    use_container_width=True
                ):
                    st.session_state[state_key] = opt1["val"]
                    st.rerun()

            with c2:
                is_active = (st.session_state[state_key] == opt2["val"])
                card_text = f"**{opt2['label']}**\n\n{opt2['sub']}"
                st.markdown('<div class="choice-box"></div>', unsafe_allow_html=True)
                if st.button(
                    card_text,
                    key=f"{state_key}_2",
                    type="primary" if is_active else "secondary",
                    use_container_width=True
                ):
                    st.session_state[state_key] = opt2["val"]
                    st.rerun()
            st.write("")

        render_clickable_card_choice(
            "1. 카페인 수혈이 필요한가요?", "caffeine",
            {"val": True, "label": "카페인 필수", "sub": "졸음 퇴치 · 집중력 유지"},
            {"val": False, "label": "논카페인", "sub": "오늘 밤 숙면 예약"}
        )
        render_clickable_card_choice(
            "2. 온도는 어떻게 할까요?", "temp",
            {"val": "ICE", "label": "무조건 ICE", "sub": "시원한 청량감"},
            {"val": "HOT", "label": "따뜻한 HOT", "sub": "속이 편안한 온기"}
        )
        render_clickable_card_choice(
            "3. 달달한 게 필요한가요?", "sweet",
            {"val": True, "label": "달달함 필요", "sub": "당 충전 · 스트레스 해소"},
            {"val": False, "label": "깔끔 · 담백", "sub": "단맛 없이 깔끔한 뒷맛"}
        )
        render_clickable_card_choice(
            "4. 우유가 들어간 메뉴?", "milk",
            {"val": True, "label": "우유 포함", "sub": "부드럽고 고소한 라떼류"},
            {"val": False, "label": "우유 없음", "sub": "가볍고 산뜻한 블랙 · 티"}
        )

        st.divider()

        st.markdown("#### 지금 어느 역 근처인가요?")
        selected_station = st.selectbox(
            "서울 지하철역 선택",
            SEOUL_STATIONS,
            index=SEOUL_STATIONS.index("충무로역")
        )
        st.session_state.station = selected_station

        if selected_station in STATION_CAFES:
            nearby_cafes = STATION_CAFES[selected_station]
        else:
            nearby_cafes = [
                {"brand": "스타벅스", "branch": f"{selected_station} 인근점"},
                {"brand": "메가MGC커피", "branch": f"{selected_station} 인근점"},
                {"brand": "컴포즈커피", "branch": f"{selected_station} 인근점"},
                {"brand": "투썸플레이스", "branch": f"{selected_station} 인근점"},
                {"brand": "매머드커피", "branch": f"{selected_station} 인근점"},
            ]

        cafe_options = [f"{c['brand']} · {c['branch']}" for c in nearby_cafes]
        selected_cafe_str = st.selectbox("가까운 카페 매장을 선택하세요", cafe_options)
        selected_brand = selected_cafe_str.split(" · ")[0]

        st.write("")
        st.markdown('<div class="submit-btn"></div>', unsafe_allow_html=True)
        if st.button(f"{selected_brand} 추천 메뉴 확인하기", use_container_width=True):
            matched = [
                d for d in DRINKS
                if d["brand"] == selected_brand
                and d["caffeine"] == st.session_state.caffeine
                and d["temp"] == st.session_state.temp
                and d["sweet"] == st.session_state.sweet
                and d["milk"] == st.session_state.milk
            ]
            if not matched:
                matched = [
                    d for d in DRINKS
                    if d["brand"] == selected_brand
                    and d["caffeine"] == st.session_state.caffeine
                    and d["temp"] == st.session_state.temp
                ]
            if not matched:
                matched = [
                    d for d in DRINKS
                    if d["brand"] == selected_brand
                    and d["caffeine"] == st.session_state.caffeine
                ]
            if not matched:
                matched = [d for d in DRINKS if d["brand"] == selected_brand]

            st.session_state.result_drink = random.choice(matched)
            st.session_state.selected_branch_str = selected_cafe_str

        if st.session_state.result_drink:
            res = st.session_state.result_drink
            nutri = res["nutrition"]
            st.divider()

            st.markdown(f"""
                <div class="drink-hero-box">
                    <div style="color: #3B4D2B; font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;">
                        {st.session_state.selected_branch_str}
                    </div>
                    {get_drink_illustration(res['illust'])}
                    <h2 style="color: #A62626; margin: 10px 0 4px 0;">{res['name']}</h2>
                    <p style="color: #6E5849; font-size: 0.85rem; margin: 0;">오늘 컨디션에 맞춰 고른 추천 음료</p>
                </div>
            """, unsafe_allow_html=True)

            with st.expander("영양성분 정보 보기 (칼로리 · 카페인 · 당 · 단백질 · 지방)", expanded=False):
                n1, n2, n3, n4, n5 = st.columns(5)
                n1.metric("칼로리", f"{nutri['kcal']} kcal")
                n2.metric("카페인", f"{nutri['caffeine']} mg")
                n3.metric("당류", f"{nutri['sugar']} g")
                n4.metric("단백질", f"{nutri['protein']} g")
                n5.metric("지방", f"{nutri['fat']} g")
                st.caption("기본 레귤러(Tall) 사이즈 기준 평균 영양성분이며, 시럽이나 우유 변경 시 달라질 수 있습니다.")

            map_query = urllib.parse.quote(f"{selected_station} {selected_brand}")
            st.link_button(f"네이버 지도로 '{selected_station} {selected_brand}' 위치 보기", f"https://map.naver.com/p/search/{map_query}", use_container_width=True)

# ==============================================================================
# [페이지 2] 요즘 바이럴 메뉴
# ==============================================================================
elif menu_page == "요즘 바이럴 메뉴":
    st.markdown("<h2 style='color: #2E1B11;'>요즘 직장인 사이 바이럴 메뉴</h2>", unsafe_allow_html=True)
    st.caption("오피스 상권에서 지금 가장 주문율이 높은 화제의 메뉴 모음")
    st.divider()

    viral_list = [
        {"brand": "스타벅스", "menu": "말차 글레이즈드 티 라떼", "tag": "꾸덕크림 · 달콤쌉쌀",
         "desc": "진한 제주 말차 라떼 위에 쫀득한 글레이즈드 폼과 말차 파우더가 올라간 시즌 인기 메뉴."},
        {"brand": "메가MGC커피", "menu": "왕메가 딸기라떼 · 할메가미숫커피", "tag": "가성비 · 오후 당 충전",
         "desc": "점심시간 식곤증을 한 번에 날려버리는 대용량 달달함으로 직장인 선호도가 높은 메뉴."},
        {"brand": "컴포즈커피", "menu": "아인슈페너 라떼", "tag": "크림맛집 · 가성비",
         "desc": "개인 카페 못지않은 쫀쫀한 우유 크림 퀄리티로 입소문 난 컴포즈 대표 추천 메뉴."},
        {"brand": "투썸플레이스", "menu": "아이스박스 쉐이크", "tag": "마시는 케이크 · 진한 단맛",
         "desc": "투썸 시그니처 케이크 아이스박스를 그대로 갈아 넣어 마스카포네 크림과 쿠키가 씹히는 메뉴."}
    ]

    for item in viral_list:
        st.markdown(f"""
            <div class="recipe-card">
                <span style="background-color: #FDF2EC; color: #A62626; padding: 3px 8px; border-radius: 6px; font-size: 0.78rem; font-weight: 700;">{item['brand']}</span>
                <span style="color: #3B4D2B; font-size: 0.8rem; font-weight: 600; margin-left: 6px;">{item['tag']}</span>
                <h4 style="margin: 8px 0 4px 0; color: #2E1B11;">{item['menu']}</h4>
                <p style="margin: 0; color: #5C4E46; font-size: 0.9rem;">{item['desc']}</p>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# [페이지 3] 꿀조합 커스텀 레시피
# ==============================================================================
elif menu_page == "꿀조합 커스텀 레시피":
    st.markdown("<h2 style='color: #2E1B11;'>실패 없는 프랜차이즈 커스텀 레시피</h2>", unsafe_allow_html=True)
    st.caption("키오스크와 모바일 오더에서 그대로 따라 선택하기만 하면 되는 검증된 커스텀")
    st.divider()

    custom_list = [
        {"brand": "스타벅스", "title": "저칼로리 고단백 두유 바닐라 라떼", "base": "아이스 카페 라떼 (Tall)",
         "steps": ["원두: 블론드 원두 변경 (무료)", "우유: 두유로 변경 (무료)", "시럽: 바닐라 시럽 1~2펌프 추가"],
         "note": "당류는 절반으로 줄이고 고소함은 살린 식단 관리 직장인 추천 레시피"},
        {"brand": "스타벅스", "title": "복숭아 아이스티 샷 추가 (스벅 버전)", "base": "아이스 블랙 티 (Tall)",
         "steps": ["시럽: 클래식 시럽 빼기", "추가: 복숭아 베이스 추가 + 에스프레소 1샷 추가"],
         "note": "일반 복숭아 아이스티보다 깔끔하고 깊은 홍차 베이스 아샷추"},
        {"brand": "메가MGC커피", "title": "초코 젤라또 아인슈페너", "base": "아이스 아메리카노",
         "steps": ["얼음: 얼음 적게", "토핑: 초코 젤라또 추가 + 휘핑크림 추가"],
         "note": "합리적인 가격으로 즐기는 꾸덕한 아포가토 스타일 디저트 커피"}
    ]

    for c in custom_list:
        steps_html = "".join([f"<li style='margin-bottom: 3px;'>{s}</li>" for s in c["steps"]])
        st.markdown(f"""
            <div class="recipe-card" style="border-left-color: #A62626;">
                <span style="background-color: #E8EDE4; color: #3B4D2B; padding: 3px 8px; border-radius: 6px; font-size: 0.78rem; font-weight: 700;">{c['brand']}</span>
                <h4 style="margin: 8px 0 4px 0; color: #2E1B11;">{c['title']}</h4>
                <div style="font-size: 0.85rem; color: #6E5849; margin-bottom: 8px;">베이스 음료: <b>{c['base']}</b></div>
                <ul style="margin: 0 0 8px 18px; padding: 0; color: #2E1B11; font-size: 0.9rem;">{steps_html}</ul>
                <div style="font-size: 0.82rem; color: #A62626; font-weight: 600;">{c['note']}</div>
            </div>
        """, unsafe_allow_html=True)