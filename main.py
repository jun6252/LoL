import streamlit as st
import random
import time
import pandas as pd
import os

# CSV 파일 이름
SCORE_FILE = "scores.csv"

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

# 단어 + 힌트 (모든 주제 섞기)
WORDS = [
    ("피셜", "자기 주장 (Official)"),
    ("갑분싸", "갑자기 분위기 싸해짐"),
    ("TMI", "너무 많은 정보"),
    ("OOTD", "오늘의 옷차림"),
    ("JMT", "정말 맛있다"),
    ("등잔 밑이 어둡다", "가까운 곳일수록 모른다"),
    ("가는 말이 고와야 오는 말이 곱다", "상대에게 예의 지켜야"),
    ("호랑이도 제 말하면 온다", "누구 이야기하면 나타난다"),
    ("하늘의 별 따기", "매우 어려운 일"),
    ("백문이 불여일견", "백 번 듣는 것보다 보기"),
    ("냉장고", "음식 보관 가전"),
    ("치약", "이를 닦을 때 씀"),
    ("지하철", "도심 대중교통"),
    ("물병", "물을 담는 용기"),
    ("전화기", "통화하는 기기")
]

# 세션 초기화
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.name = ""
    st.session_state.word_list = []
    st.session_state.current_word = None
    st.session_state.hint = ""
    st.session_state.start_time = None
    st.session_state.score = 0
    st.session_state.problem_start_time = None
    st.session_state.show_hint = False
    st.session_state.game_over = False

# 게임 시작 전
if not st.session_state.started:
    st.title("⚡ 스피드 초성 퀴즈")
    st.markdown("20초 안에 최대한 많이 맞혀보세요!")

    name = st.text_input("당신의 이름을 입력하세요:")
    if st.button("게임 시작!") and name.strip():
        st.session_state.name = name.strip()
        st.session_state.word_list = WORDS.copy()
        random.shuffle(st.session_state.word_list)
        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.start_time = time.time()
        st.session_state.problem_start_time = time.time()
        st.session_state.score = 0
        st.session_state.show_hint = False
        st.session_state.started = True
        st.rerun()
    elif st.button("게임 시작!") and not name.strip():
        st.warning("이름을 입력하세요.")

# 게임 진행 중
elif not st.session_state.game_over:
    now = time.time()
    elapsed = now - st.session_state.start_time
    remaining = 20 - elapsed

    if remaining <= 0:
        st.session_state.game_over = True
        st.rerun()

    st.title("🔥 스피드 퀴즈 중!")
    st.markdown(f"⏱️ 남은 시간: **{int(remaining)}초**")
    st.markdown(f"🏆 현재 점수: **{st.session_state.score}개**")

    initials = get_initials(st.session_state.current_word)
    st.markdown(f"### 🔤 초성: **{initials}**")

    if not st.session_state.show_hint and now - st.session_state.problem_start_time >= 5:
        st.session_state.show_hint = True

    if st.session_state.show_hint:
        st.info(f"💡 힌트: {st.session_state.hint}")

    answer = st.text_input("정답:", key=str(now))

    if st.button("제출"):
        if answer.strip() == st.session_state.current_word:
            st.success("🎉 정답!")
            st.session_state.score += 1
        else:
            st.warning("❌ 틀렸지만 넘어갑니다!")

        if not st.session_state.word_list:
            st.session_state.word_list = WORDS.copy()
            random.shuffle(st.session_state.word_list)

        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.rerun()

# 게임 종료 후
else:
    st.title("🏁 게임 종료!")
    st.markdown(f"👏 **{st.session_state.name}님**, 점수는 **{st.session_state.score}점** 입니다!")

    # 점수 저장
    new_data = pd.DataFrame([{
        "이름": st.session_state.name,
        "점수": st.session_state.score
    }])

    if os.path.exists(SCORE_FILE):
        old_data = pd.read_csv(SCORE_FILE)
        df = pd.concat([old_data, new_data], ignore_index=True)
    else:
        df = new_data

    df = df.sort_values(by="점수", ascending=False).reset_index(drop=True)
    df.to_csv(SCORE_FILE, index=False)

    # 랭킹표 출력
    st.markdown("## 🏆 전체 랭킹")
    st.dataframe(df.head(10))

    if st.button("🔄 다시 하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
