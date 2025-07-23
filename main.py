import streamlit as st
import random
import re

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

# 단어 리스트
WORDS = [
    "사과", "학교", "컴퓨터", "자동차", "의자", "물고기",
    "바나나", "선생님", "강아지", "치킨", "냉장고", "호랑이",
    "공부", "연필", "핸드폰", "텔레비전", "고양이"
]

# 세션 초기화
if "word" not in st.session_state:
    st.session_state.word = random.choice(WORDS)
    st.session_state.solved = False

# UI
st.title("🧠 초성 퀴즈 게임")
st.markdown("초성을 보고 어떤 단어인지 맞혀보세요!")

if not st.session_state.solved:
    initials = get_initials(st.session_state.word)
    st.markdown(f"### 🔤 초성: **{initials}**")

    answer = st.text_input("정답을 입력하세요:", key="answer_input")

    if st.button("제출"):
        if answer.strip() == st.session_state.word:
            st.success("🎉 정답입니다!")
            st.session_state.solved = True
        else:
            st.error("❌ 틀렸습니다. 다시 시도해보세요.")
else:
    st.markdown(f"정답은 **{st.session_state.word}** 였습니다.")
    if st.button("🔄 다시 시작"):
        st.session_state.word = random.choice(WORDS)
        st.session_state.solved = False
        st.experimental_rerun()
