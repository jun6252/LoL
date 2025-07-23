import streamlit as st
import random
import time

# 🔊 효과음 재생
def play_success():
    st.markdown(
        """
        <audio autoplay>
        <source src="https://actions.google.com/sounds/v1/cartoon/concussive_drum_hit.ogg" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True,
    )

def play_fail():
    st.markdown(
        """
        <audio autoplay>
        <source src="https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# 🎯 난이도 설정
difficulty_levels = {
    "쉬움": 10,
    "보통": 5,
    "어려움": 2.5,
}

# 🧠 세션 상태 초기화
if "stairs" not in st.session_state:
    st.session_state.stairs = []
    st.session_state.position = 0
    st.session_state.last_foot = None
    st.session_state.game_over = False
    st.session_state.start_time = None
    st.session_state.limit = None

# 🎮 난이도 선택
difficulty = st.selectbox("난이도를 선택하세요", list(difficulty_levels.keys()))

# 🧱 계단 생성
def generate_stairs(n=30):
    st.session_state.stairs = [random.choice(["L", "R"]) for _ in range(n)]

# ▶ 게임 시작
if st.button("게임 시작", type="primary"):
    generate_stairs()
    st.session_state.position = 0
    st.session_state.last_foot = None
    st.session_state.game_over = False
    st.session_state.start_time = time.time()
    st.session_state.limit = difficulty_levels[difficulty]

# ⏱️ 시간 초과 체크
if st.session_state.start_time and not st.session_state.game_over:
    elapsed = time.time() - st.session_state.start_time
    if elapsed > st.session_state.limit:
        st.session_state.game_over = True
        play_fail()
        st.warning(f"⏱️ 시간 초과! {st.session_state.limit}초 초과됨")

# 🪜 계단 그리기
st.markdown("### 🪜 무한의 계단")
if st.session_state.stairs:
    for i in range(len(st.session_state.stairs)-1, -1, -1):
        if i == st.session_state.position:
            st.markdown(f"🧍‍♂️ **[{i+1}] {st.session_state.stairs[i]}**")
        else:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[{i+1}] {st.session_state.stairs[i]}")

# 👣 왼발/오른발 버튼
if not st.session_state.game_over and st.session_state.stairs:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("왼발"):
            if st.session_state.last_foot == 'L':
                st.session_state.game_over = True
                play_fail()
            elif st.session_state.stairs[st.session_state.position] == 'L':
                st.session_state.position += 1
                st.sessio
