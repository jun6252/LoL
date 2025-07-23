import streamlit as st
import random
import time

# 무서운 사진 URL 리스트
SCARY_IMAGES = [
    "https://i.pinimg.com/originals/...ghostface1.jpg",  # 예시 Ghostface
    "https://image-stock/...scream_face2.jpg",
    "https://pinimg.com/...creepy_child3.jpg",
    "https://pngtree.com/...eerie_woman4.jpg"
]
SCREAM_AUDIO_URL = "https://cdn.pixabay.com/download/audio/2022/03/15/audio_88b4f116d7.mp3?filename=scream-143121.mp3"

def reset_game():
    st.session_state.bridge = [random.choice(["L","R"]) for _ in range(15)]
    st.session_state.current_step = 0
    st.session_state.game_over = False
    st.session_state.cleared = False

if "bridge" not in st.session_state:
    reset_game()

st.title("🦇 징검다리 공포게임 (15칸)")

with st.expander("🛣️ 진행 상황", expanded=True):
    marks = []
    for idx in range(15):
        if idx < st.session_state.current_step:
            marks.append("✅")
        elif idx == st.session_state.current_step and not st.session_state.game_over:
            marks.append("❓")
        else:
            marks.append("⬜")
    st.markdown(" ".join(marks))

if st.session_state.game_over:
    st.error("💀 틀렸습니다... 공포 출현!")
    img_url = random.choice(SCARY_IMAGES)
    st.image(img_url, caption="으아악!!!", use_column_width=True)
    st.audio(SCREAM_AUDIO_URL, format="audio/mp3", autoplay=True)
    time.sleep(3)
    reset_game()
    st.experimental_rerun()

elif st.session_state.cleared:
    st.success("🎉 성공! 다리를 모두 건넜습니다!")
    if st.button("🔁 다시 시작"):
        reset_game()
        st.experimental_rerun()
else:
    st.subheader(f"{st.session_state.current_step+1}번째 칸, 왼(L) or 오(R) 선택:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 왼쪽 (L)"):
            if st.session_state.bridge[st.session_state.current_step] == "L":
                st.session_state.current_step += 1
            else:
                st.session_state.game_over = True
    with col2:
        if st.button("➡️ 오른쪽 (R)"):
            if st.session_state.bridge[st.session_state.current_step] == "R":
                st.session_state.current_step += 1
            else:
                st.session_state.game_over = True
    if st.session_state.current_step == len(st.session_state.bridge):
        st.session_state.cleared = True
        st.experimental_rerun()
