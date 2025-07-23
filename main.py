import streamlit as st
import random
import time
import pandas as pd
import os

SCORE_FILE = "scores.csv"
LIMIT_TIME = 45

# 초성 추출 함수
def get_initials(word):
    CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    result = ""
    for char in word:
        if '가' <= char <= '힣':
            code = ord(char) - ord('가')
            result += CHOSUNG_LIST[code // 588]
        else:
            result += char
    return result

# 제시어 리스트
WORDS = [
    ("냉장고", "음식을 차갑게 보관하는 기기"), ("치약", "이를 닦는 데 쓰는 물건"),
    ("지하철", "도시 대중교통"), ("우산", "비 올 때 쓰는 물건"),
    ("책상", "공부나 일을 위한 가구"), ("선풍기", "바람을 일으키는 기기"),
    ("강아지", "멍멍 짖는 반려동물"), ("고양이", "야옹하는 반려동물"),
    ("우물 안 개구리", "세상 물정을 모르는 사람"), ("하늘의 별 따기", "매우 어려운 일"),
    ("호랑이도 제 말하면 온다", "누구 이야기하면 나타난다"), ("가는 말이 고와야 오는 말이 곱다", "예의는 서로 지켜야 한다"),
    ("백문이 불여일견", "백 번 듣는 것보다 한 번 보는 게 낫다"), ("돌다리도 두들겨 보고 건너라", "확실한 것도 확인해야 한다"),
    ("티끌 모아 태산", "작은 것도 모이면 커짐")
]

# 상태 초기화
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.name = ""
    st.session_state.word_list = []
    st.session_state.current_word = ""
    st.session_state.hint = ""
    st.session_state.score = 0
    st.session_state.start_time = 0.0
    st.session_state.problem_start_time = 0.0
    st.session_state.show_hint = False
    st.session_state.game_over = False

# 시작 화면
if not st.session_state.started:
    st.title("⚡ 초성 스피드 퀴즈")
    name = st.text_input("이름을 입력하세요:")
    if st.button("게임 시작"):
        if not name.strip():
            st.warning("이름을 입력해주세요.")
        else:
            st.session_state.name = name.strip()
            st.session_state.word_list = WORDS.copy()
            random.shuffle(st.session_state.word_list)
            st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.problem_start_time = time.time()
            st.session_state.show_hint = False
            st.session_state.started = True
            st.experimental_rerun()

# 게임 진행
elif not st.session_state.game_over:
    now = time.time()
    elapsed = now - st.session_state.start_time
    remaining = int(LIMIT_TIME - elapsed)

    if remaining <= 0:
        st.session_state.game_over = True
        st.experimental_rerun()

    color = "green" if remaining > 30 else "orange" if remaining > 15 else "red"
    st.markdown(f"<h4 style='color:{color}'>⏱ 남은 시간: {remaining}초</h4>", unsafe_allow_html=True)
    st.markdown(f"🏆 현재 점수: **{st.session_state.score}개**")

    initials = get_initials(st.session_state.current_word)
    st.markdown(f"### 🔤 초성: **{initials}**")

    if not st.session_state.show_hint and now - st.session_state.problem_start_time >= 3:
        st.session_state.show_hint = True

    answer = st.text_input("정답 입력:", key="answer")

    if st.session_state.show_hint:
        st.markdown(f"<div style='color:gray; margin-top:-10px;'>💡 힌트: {st.session_state.hint}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    if col1.button("제출"):
        if answer.strip() == st.session_state.current_word:
            st.success("🎉 정답입니다!")
            st.session_state.score += 1
        else:
            st.warning("❌ 오답입니다. 다음 문제로 넘어갑니다.")

        if not st.session_state.word_list:
            st.session_state.word_list = WORDS.copy()
            random.shuffle(st.session_state.word_list)

        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.experimental_rerun()

    if col2.button("패스"):
        if not st.session_state.word_list:
            st.session_state.word_list = WORDS.copy()
            random.shuffle(st.session_state.word_list)

        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.experimental_rerun()

# 게임 종료
else:
    st.title("🏁 게임 종료!")
    st.markdown(f"**{st.session_state.name}**님의 점수는 **{st.session_state.score}점**입니다.")

    if os.path.exists(SCORE_FILE):
        df = pd.read_csv(SCORE_FILE)
        df = df[df["이름"] != st.session_state.name]
    else:
        df = pd.DataFrame(columns=["이름", "점수"])

    new_row = pd.DataFrame([{"이름": st.session_state.name, "점수": st.session_state.score}])
    df = pd.concat([df, new_row], ignore_index=True)
    df = df.sort_values(by="점수", ascending=False).reset_index(drop=True)
    df.to_csv(SCORE_FILE, index=False)

    st.markdown("## 🏆 랭킹")
    st.dataframe(df.head(10))

    if st.button("🔁 다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
