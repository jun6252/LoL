import streamlit as st
import random

# 초기화
if 'stairs' not in st.session_state:
    st.session_state.stairs = []  # 계단 방향 리스트 (L/R)
    st.session_state.position = 0  # 현재 위치
    st.session_state.last_foot = None  # 마지막 발
    st.session_state.game_over = False

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

