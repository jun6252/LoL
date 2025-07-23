import streamlit as st
import random
from PIL import Image
import time

# 설정
st.set_page_config(page_title="징검다리 공포게임", layout="centered")

# 게임 초기화 함수
def reset_game():
    st.session_state.bridge = [random.choice(["L", "R"]) for _ in range(15)]
    st.session_state.current_step = 0
    st.session_state.game_over = False
    st.session_state.cleared = False

# 초기화
if "bridge" not in st.session_state:
    reset_game()

# 제목
st.title("🦑 징검다리 공포게임")
st.markdown("15개의 칸을 건너세요. 실패하면... 무언가가 나타납니다 😱")

# 진행 상황 시각화
with st.expander("현재 징검다리 진행 상황", expanded=True):
    bridge_display = []
    for i in range(len(st.session_state.bridge)):
        if i < st.session_state.current_step:
            bridge_display.append("✅")
        elif i == st.session_state.current_step and not st.session_state.game_over:
            bridge_display.append("❓")
        else:
            bridge_display.append("⬜")
    st.markdown(" ".join(bridge_display))

# 실패 처리
if st.session_state.game_over:
    st.error("💀 틀렸습니다... 게임 오버!")

    # 무서운 사진 + 효과음
    image = Image.open("ghost.jpg")
    st.image(image, caption="으아악!!!", use_column_width=True)
    st.audio("scream.mp3", autoplay=True)

    # 잠깐 멈췄다가 자동 초기화
    time.sleep(3)
    st.warning("게임이 초기화됩니다...")
    time.sleep(1)
    reset_game()
    st.experimental_rerun()

# 클리어 처리
elif st.session_state.cleared:
    st.success("🎉 축하합니다! 다리를 모두 건넜습니다!")
    if st.button("🔁 다시 시작"):
        reset_game()
        st.experimental_rerun()

# 진행 중
else:
    st.subheader(f"{st.session_state.current_step + 1}번째 칸 - 선택하세요:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 왼쪽 (L)"):
            choice = "L"
            answer = st.session_state.bridge[st.session_state.current_step]
            if choice == answer:
                st.session_state.current_step += 1
            else:
                st.session_state.game_over = True

    with col2:
        if st.button("➡️ 오른쪽 (R)"):
            choice = "R"
            answer = st.session_state.bridge[st.session_state.current_step]
            if choice == answer:
                st.session_state.current_step += 1
            else:
                st.session_state.game_over = True

    # 클리어 체크
    if st.session_state.current_step == len(st.session_state.bridge):
        st.session_state.cleared = True
        st.experimental_rerun()
