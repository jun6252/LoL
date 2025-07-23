import streamlit as st
import random
import time

# 초성 추출 함수
def get_initials(word):
    CHOSUNG_LIST = [
        'ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ',
        'ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
    ]
    initials = ""
    for char in word:
        if '가' <= char <= '힣':
            code = ord(char) - ord('가')
            cho = code // 588
            initials += CHOSUNG_LIST[cho]
        else:
            initials += char
    return initials

# 주제별 단어와 힌트
WORDS = {
    "줄임말": [
        ("피셜", "자기 'Official' 주장이라는 뜻"),
        ("갑분싸", "갑자기 분위기 싸해짐"),
        ("TMI", "너무 많은 정보"),
        ("OOTD", "오늘의 옷차림"),
        ("JMT", "정말 맛있다")
    ],
    "속담": [
        ("등잔 밑이 어둡다", "가까운 곳의 사정을 오히려 모른다"),
        ("가는 말이 고와야 오는 말이 곱다", "상대에게 예의를 지켜야 한다"),
        ("호랑이도 제 말하면 온다", "누구 이야기하면 나타난다"),
        ("하늘의 별 따기", "매우 어렵다"),
        ("백문이 불여일견", "백 번 듣는 것보다 한 번 보는 게 낫다")
    ],
    "일상생활": [
        ("냉장고", "음식을 시원하게 보관하는 가전"),
        ("치약", "이를 닦을 때 쓰는 것"),
        ("지하철", "도심 대중교통 수단"),
        ("물병", "물을 담는 용기"),
        ("전화기", "멀리 있는 사람과 통화")
    ]
}

# 세션 초기화
if "category" not in st.session_state:
    st.session_state.category = None
    st.session_state.word = None
    st.session_state.hint = None
    st.session_state.start_time = None
    st.session_state.solved = False
    st.session_state.show_hint = False

# 게임 시작 또는 카테고리 선택
if not st.session_state.category:
    st.title("🧠 초성 퀴즈 게임")
    st.subheader("주제를 선택하세요!")
    category = st.selectbox("주제", list(WORDS.keys()))
    if st.button("게임 시작"):
        st.session_state.category = category
        st.session_state.word, st.session_state.hint = random.choice(WORDS[category])
        st.session_state.start_time = time.time()
        st.session_state.solved = False
        st.session_state.show_hint = False
        st.rerun()

else:
    st.title(f"🧠 [{st.session_state.category}] 초성 퀴즈")
    initials = get_initials(st.session_state.word)
    st.markdown(f"### 🔤 초성: **{initials}**")

    # 시간 경과 체크
    if not st.session_state.solved:
        elapsed = time.time() - st.session_state.start_time
        if elapsed >= 10 and not st.session_state.show_hint:
            st.session_state.show_hint = True
            st.warning("⌛ 시간이 초과되었습니다! 힌트를 드릴게요.")

    if st.session_state.show_hint:
        st.info(f"💡 힌트: {st.session_state.hint}")

    answer = st.text_input("정답을 입력하세요:")

    if st.button("제출") and not st.session_state.solved:
        if answer.strip() == st.session_state.word:
            st.success("🎉 정답입니다!")
            st.session_state.solved = True
        else:
            st.error("❌ 틀렸습니다. 다시 시도해보세요.")

    if st.session_state.solved:
        if st.button("🔄 다음 문제"):
            st.session_state.word, st.session_state.hint = random.choice(WORDS[st.session_state.category])
            st.session_state.solved = False
            st.session_state.show_hint = False
            st.session_state.start_time = time.time()
            st.rerun()

    if st.button("🏠 주제로 돌아가기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
