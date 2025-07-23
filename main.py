import streamlit as st
import random

# 초기화
if 'stairs' not in st.session_state:
    st.session_state.stairs = []  # 계단 방향 리스트 (L/R)
    st.session_state.position = 0  # 현재 위치
    st.session_state.last_foot = None  # 마지막 발
    st.session_state.game_over = Falseimport streamlit as st
import random
import time

# 효과음 삽입 함수
def play_sound():
    st.markdown(
        """
        <audio autoplay>
        <source src="https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# 난이도 설정 (초 단위 제한시간)
difficulty_levels = {
    "쉬움": 10,
    "보통": 5,
    "어려움": 2.5,
}

# 초기화
if "stairs" not in st.session_state:
    st.session_state.stairs = []
    st.session_state.position = 0
    st.session_state.last_foot = None
    st.session_state.game_over = False
    st.session_state.start_time = None
    st.session_state.limit = None

# 난이도 선택
difficulty = st.selectbox("난이도를 선택하세요", list(difficulty_levels.keys()))

# 계단 생성
def generate_stairs(n=30):
    st.session_state.stairs = [random.choice(["L", "R"]) for _ in range(n)]

if st.button("게임 시작", type="primary"):
    generate_stairs()
    st.session_state.position = 0
    st.session_state.last_foot = None
    st.session_state.game_over = False
    st.session_state.start_time = time.time()
    st.session_state.limit = difficulty_levels[difficulty]

st.markdown("### 🪜 무한의 계단")

# 시간 초과 체크
if st.session_state.start_time and not st.session_state.game_over:
    elapsed = time.time() - st.session_state.start_time
    if elapsed > st.session_state.limit:
        st.session_state.game_over = True
        st.warning(f"⏱️ 시간 초과! 제한 {st.session_state.limit}초 초과됨")

# 계단 표시
if st.session_state.stairs:
    for i in range(len(st.session_state.stairs)-1, -1, -1):
        if i == st.session_state.position:
            st.markdown(f"🧍‍♂️ **[{i+1}] {st.session_state.stairs[i]}**")
        else:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[{i+1}] {st.session_state.stairs[i]}")

# 발판 버튼
if not st.session_state.game_over and st.session_state.stairs:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("왼발"):
            if st.session_state.last_foot == 'L':
                st.session_state.game_over = True
            elif st.session_state.stairs[st.session_state.position] == 'L':
                st.session_state.position += 1
                st.session_state.last_foot = 'L'
                st.session_state.start_time = time.time()  # 성공시 시간 리셋
                play_sound()
            else:
                st.session_state.game_over = True
    with col2:
        if st.button("오른발"):
            if st.session_state.last_foot == 'R':
                st.session_state.game_over = True
            elif st.session_state.stairs[st.session_state.position] == 'R':
                st.session_state.position += 1
                st.session_state.last_foot = 'R'
                st.session_state.start_time = time.time()
                play_sound()
            else:
                st.session_state.game_over = True

# 게임 오버 메시지
if st.session_state.game_over:
    st.error("❌ 게임 오버! 다시 시작하세요.")

# 게임 클리어
if st.session_state.position >= len(st.session_state.stairs):
    st.success("🎉 축하합니다! 계단을 완주했어요!")


# 계단 생성
def generate_stairs(n=30):
    st.session_state.stairs = [random.choice(['L', 'R']) for _ in range(n)]

if st.button("게임 시작", type="primary"):
    generate_stairs()
    st.session_state.position = 0
    st.session_state.last_foot = None
    st.session_state.game_over = False

st.markdown("### 무한의 계단")

# 계단 그리기
if st.session_state.stairs:
    for i in range(len(st.session_state.stairs)-1, -1, -1):
        if i == st.session_state.position:
            st.markdown(f"🧍‍♂️ **[{i+1}] {st.session_state.stairs[i]}**")
        else:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[{i+1}] {st.session_state.stairs[i]}")

# 게임 오버 여부 확인
if st.session_state.game_over:
    st.error("❌ 게임 오버! 다시 시작하세요.")
else:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("왼발", use_container_width=True):
            if st.session_state.last_foot == 'L':
                st.session_state.game_over = True
            elif st.session_state.stairs[st.session_state.position] == 'L':
                st.session_state.position += 1
                st.session_state.last_foot = 'L'
            else:
                st.session_state.game_over = True
    with col2:
        if st.button("오른발", use_container_width=True):
            if st.session_state.last_foot == 'R':
                st.session_state.game_over = True
            elif st.session_state.stairs[st.session_state.position] == 'R':
                st.session_state.position += 1
                st.session_state.last_foot = 'R'
            else:
                st.session_state.game_over = True

    # 게임 클리어
    if st.session_state.position >= len(st.session_state.stairs):
        st.success("🎉 축하합니다! 계단을 완주했어요!")

