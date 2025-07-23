import streamlit as st
import random
import time

# 네가 업로드한 이미지 파일명 (15개)
SCARY_IMAGES = [
    "8b6a356c-fc12-44e3-afcf-ae7aecf5ca51.png",
    "743ce748-6b5f-4550-a89b-7f74e7b8bc0e.png",
    "88e49919-b319-44f5-86c2-cd4f0e7f5bc5.png",
    "4aacb2ee-8fe7-42fc-a032-52e53f1df59e.png",
    "a0909e56-6f4a-45a1-9f7e-7924edd44acb.png",
    "b9de195c-2519-4d13-83ac-fafd59ca519a.png",
    "f7c67c74-02ef-49d3-8746-774e739f5c6e.png",
    "c10023fd-d27f-4573-96a7-75f1814ce398.png",
    "52c9e878-2152-44ab-b96a-bf502b309aa2.png",
    "6f2985cc-69b3-4a48-ac31-613628e3d4c2.png",
    "4f27933e-c3dc-4637-8f7a-6ae0b0bc280e.png",
    "b189585a-4d67-41e7-9052-ce77f93db120.png",
    "bf2f8987-fd2b-4ebf-89ca-b9997b2d0e88.png",
    "0de9e869-154c-48b0-8cb2-755681722df7.png",
    "3ed983c9-72df-4d5c-a71c-84348b90d09b.png",
]

# 공포 효과음 mp3 (Pixabay 공개 음원)
SCARY_SOUNDS = {
    "귀신 속삭임": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_88b4f116d7.mp3?filename=scream-143121.mp3",
    "기괴한 속삭임": "https://cdn.pixabay.com/download/audio/2022/11/07/audio_d0c87dc8b8.mp3?filename=whispering-ambient-124737.mp3",
    "악몽 비명": "https://cdn.pixabay.com/download/audio/2023/03/06/audio_0d68b91a5b.mp3?filename=nightmare-scream-140172.mp3",
    "공포 브레이크": "https://cdn.pixabay.com/download/audio/2022/03/01/audio_bfa2b13222.mp3?filename=horror-stinger-133129.mp3",
    "지옥문 오픈": "https://cdn.pixabay.com/download/audio/2021/08/09/audio_84de31ec6c.mp3?filename=gate-of-hell-8825.mp3",
    "비명과 속삭임": "https://cdn.pixabay.com/download/audio/2022/11/07/audio_3de50d4c82.mp3?filename=creepy-whisper-124739.mp3"
}

# 세션 초기화
if "bridge" not in st.session_state:
    st.session_state.bridge = [random.choice(["L", "R"]) for _ in range(15)]
    st.session_state.current_step = 0
    st.session_state.game_over = False
    st.session_state.cleared = False
    st.session_state.show_scare = False
    st.session_state.scare_image = None
    st.session_state.scare_sound = None

# 리셋 함수
def reset_game():
    st.session_state.bridge = [random.choice(["L", "R"]) for _ in range(15)]
    st.session_state.current_step = 0
    st.session_state.game_over = False
    st.session_state.cleared = False
    st.session_state.show_scare = False
    st.session_state.scare_image = None
    st.session_state.scare_sound = None

# 타이틀
st.title("👻 징검다리 공포게임")
st.markdown("왼쪽 / 오른쪽을 선택해 다리를 건너세요. 틀리면 무언가가 나옵니다...")

# 공포 화면 출력 모드
if st.session_state.show_scare:
    st.error("💀 틀렸습니다!")
    st.image(f"/mnt/data/{st.session_state.scare_image}", caption="😱", use_container_width=True)
    st.audio(st.session_state.scare_sound, autoplay=True)
    st.caption("👁 효과음 재생 중...")
    st.session_state.show_scare = False
    time.sleep(3)
    reset_game()
    st.rerun()

# 클리어
elif st.session_state.cleared:
    st.success("🎉 성공! 다 건넜습니다.")
    if st.button("🔁 다시 시작"):
        reset_game()
        st.rerun()

# 정상 진행
else:
    with st.expander("🛣️ 현재 진행 상황", expanded=True):
        progress = []
        for i in range(15):
            if i < st.session_state.current_step:
                progress.append("✅")
            elif i == st.session_state.current_step:
                progress.append("❓")
            else:
                progress.append("⬜")
        st.markdown(" ".join(progress))

    st.subheader(f"{st.session_state.current_step + 1}번째 칸 - 선택하세요:")
    col1, col2 = st.columns(2)

    def check(choice):
        correct = st.session_state.bridge[st.session_state.current_step]
        if choice == correct:
            st.session_state.current_step += 1
            if st.session_state.current_step == len(st.session_state.bridge):
                st.session_state.cleared = True
        else:
            st.session_state.game_over = True
            st.session_state.show_scare = True
            st.session_state.scare_image = random.choice(SCARY_IMAGES)
            st.session_state.scare_sound = random.choice(list(SCARY_SOUNDS.values()))

    with col1:
        if st.button("⬅️ 왼쪽 (L)"):
            check("L")
            st.rerun()
    with col2:
        if st.button("➡️ 오른쪽 (R)"):
            check("R")
            st.rerun()
