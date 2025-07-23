import streamlit as st
import random
import time

# 공포 이미지 12장
SCARY_IMAGES = [
    "https://cdn.pixabay.com/photo/2016/11/29/04/17/fear-1868619_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/01/30/21/52/horror-2029238_1280.jpg",
    "https://cdn.pixabay.com/photo/2021/10/07/16/56/ghost-6688530_1280.jpg",
    "https://cdn.pixabay.com/photo/2016/11/22/23/44/horror-1851018_1280.jpg",
    "https://cdn.pixabay.com/photo/2021/09/15/13/34/horror-6626702_1280.jpg",
    "https://cdn.pixabay.com/photo/2019/10/06/20/43/horror-4532106_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/08/31/00/16/horror-2698558_1280.jpg",
    "https://cdn.pixabay.com/photo/2015/12/01/20/28/fear-1075792_1280.jpg",
    "https://cdn.pixabay.com/photo/2018/10/25/10/32/fear-3778747_1280.jpg",
    "https://cdn.pixabay.com/photo/2021/10/28/19/08/ghost-6749319_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/10/26/22/48/halloween-2893710_1280.jpg",
    "https://cdn.pixabay.com/photo/2021/10/29/17/58/ghost-6751402_1280.jpg"
]

# TODO: 여기에 효과음 URL 6개 이상 추가해주세요
SCARY_SOUNDS = {
    "귀신 속삭임": "https://.../whisper.mp3",
    "귀신 울부짖음": "https://.../scream1.mp3",
    "공포의 불협화음": "https://.../dissonance.mp3",
    "유령 공포소리": "https://.../ghost1.mp3",
    "죽은영혼소리": "https://.../deadecho.mp3",
    "바람소리": "https://.../wind.mp3"
}

def reset_game():
    st.session_state.bridge = [random.choice(["L", "R"]) for _ in range(15)]
    st.session_state.current_step = 0
    st.session_state.game_over = False
    st.session_state.cleared = False

if "bridge" not in st.session_state:
    reset_game()

st.title("🦇 징검다리 공포게임 (15칸)")
st.markdown("틀리면 무작위 공포 이미지 + 효과음! 자동 초기화됩니다.")

with st.expander("🛣️ 진행 상황", expanded=True):
    marks = ["✅" if i < st.session_state.current_step else
             "❓" if i == st.session_state.current_step and not st.session_state.game_over else "⬜"
             for i in range(15)]
    st.markdown(" ".join(marks))

if st.session_state.game_over:
    st.error("💀 틀렸습니다! 공포 등장!")
    img = random.choice(SCARY_IMAGES)
    sound_label, sound_url = random.choice(list(SCARY_SOUNDS.items()))

    st.image(img, caption="😱", use_container_width=True)
    st.audio(sound_url, format="audio/mp3", autoplay=True)
    st.caption(f"🔊 효과음: {sound_label}")

    time.sleep(3)
    reset_game()
    st.rerun()

elif st.session_state.cleared:
    st.success("🎉 성공적으로 다리를 건넜습니다!")
    if st.button("🔁 다시 시작"):
        reset_game()
        st.rerun()

else:
    st.subheader(f"{st.session_state.current_step+1}번째 칸, L or R 선택:")
    col1, col2 = st.columns(2)
    if col1.button("⬅️ 왼쪽"):
        if st.session_state.bridge[st.session_state.current_step] == "L":
            st.session_state.current_step += 1
        else:
            st.session_state.game_over = True
    if col2.button("➡️ 오른쪽"):
        if st.session_state.bridge[st.session_state.current_step] == "R":
            st.session_state.current_step += 1
        else:
            st.session_state.game_over = True
    if st.session_state.current_step == len(st.session_state.bridge):
        st.session_state.cleared = True
        st.rerun()
