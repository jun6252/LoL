import streamlit as st
import random
import time
import pandas as pd
import os

SCORE_FILE = "scores.csv"

# 초성 추출 함수 (한글만 처리)
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
            initials += char  # 영어면 그대로
    return initials

# 한국어 + 영어 문제 100개 예시 (일부 영어 UI 표시용)
WORDS = [
    # 한국어 제시어
    ("냉장고", "음식을 차갑게 보관하는 전자제품"),
    ("지하철", "도심 속 대중교통"),
    ("치약", "이를 닦는 데 사용하는 것"),
    ("강아지", "멍멍 짖는 동물"),
    ("컴퓨터", "프로그래밍과 문서 작업 기기"),
    ("등잔 밑이 어둡다", "가까운 것을 오히려 모른다"),
    ("호랑이도 제 말하면 온다", "누구 이야기하면 나타난다"),
    ("하늘의 별 따기", "아주 어려운 일"),
    ("백문이 불여일견", "직접 보는 게 더 낫다"),
    ("가는 말이 고와야 오는 말이 곱다", "예의는 서로 지켜야 한다"),

    # 영어 제시어 (UI 영어)
    ("TMI", "Too much information"),
    ("LOL", "Laugh out loud"),
    ("ASAP", "As soon as possible"),
    ("FYI", "For your information"),
    ("DIY", "Do it yourself"),
    ("BRB", "Be right back"),
    ("OOTD", "Outfit of the day"),
    ("IDK", "I don't know"),
    ("JMT", "Jot Mas Ta (Korean slang for delicious)"),
    ("MBTI", "Myers-Briggs Type Indicator"),
] + [
    (f"Word{i}", f"Hint for Word {i}") if i % 2 == 0 else (f"단어{i}", f"{i}번째 가상의 단어 설명")
    for i in range(21, 101)
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

# 시작 화면
if not st.session_state.started:
    st.title("⚡ Speed Initial Quiz (초성 스피드 퀴즈)")
    st.markdown("🕒 30초 안에 최대한 많은 단어를 맞혀보세요!")

    name = st.text_input("이름 / Name:")
    if st.button("게임 시작 / Start"):
        if not name.strip():
            st.warning("이름을 입력하세요 / Please enter your name.")
        else:
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

# 게임 진행
elif not st.session_state.game_over:
    st.title("🔥 문제 풀이 중... / Solving...")

    now = time.time()
    elapsed = now - st.session_state.start_time
    remaining = 30 - elapsed

    if remaining <= 0:
        st.session_state.game_over = True
        st.rerun()

    st.markdown(f"⏱️ 남은 시간 / Time left: **{int(remaining)}초**")
    st.markdown(f"✅ 점수 / Score: **{st.session_state.score}개**")

    word = st.session_state.current_word
    hint = st.session_state.hint

    # UI 언어 구분
    is_korean = all('가' <= ch <= '힣' or ch.isspace() for ch in word)

    # 문제 표시
    initials = get_initials(word)
    if is_korean:
        st.markdown(f"### 🔤 초성: **{initials}**")
    else:
        st.markdown(f"### 🔡 Initials: **{initials}**")

    # 힌트 표시 (3초 경과 후)
    if not st.session_state.show_hint and now - st.session_state.problem_start_time >= 3:
        st.session_state.show_hint = True

    if st.session_state.show_hint:
        if is_korean:
            st.info(f"💡 힌트: {hint}")
        else:
            st.info(f"💡 Hint: {hint}")

    # 정답 입력
    answer = st.text_input("정답 입력 / Enter answer:", key=str(now))

    col1, col2 = st.columns(2)
    if col1.button("제출 / Submit"):
        if answer.strip().lower() == word.lower():
            st.success("🎉 정답입니다! / Correct!")
            st.session_state.score += 1
        else:
            st.warning("❌ 틀렸습니다! 다음 문제로 넘어갑니다. / Wrong! Moving on.")

        if not st.session_state.word_list:
            st.session_state.word_list = WORDS.copy()
            random.shuffle(st.session_state.word_list)

        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.rerun()

    if col2.button("패스 / Pass"):
        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.rerun()

# 게임 종료
else:
    st.title("🏁 게임 종료 / Game Over")
    st.markdown(f"🎯 **{st.session_state.name}** 님의 점수는 **{st.session_state.score}점**입니다!")

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

    st.markdown("## 🏆 랭킹 / Ranking")
    st.dataframe(df.head(10))

    if st.button("🔄 다시 하기 / Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
