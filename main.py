import streamlit as st
import random
import time
import pandas as pd
import os

SCORE_FILE = "scores.csv"
LIMIT_TIME = 45  # 제한 시간 (초)

# 초성 추출 함수
def get_initials(word):
    CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    initials = ""
    for char in word:
        if '가' <= char <= ' ' or char < '가':
            initials += char
            continue
        code = ord(char) - ord('가')
        cho = code // 588
        initials += CHOSUNG_LIST[cho]
    return initials

# 진짜 한국어 단어 + 속담만 (샘플 30개)
WORDS = [
    ("냉장고", "음식을 차갑게 보관하는 기기"), ("치약", "이를 닦는 데 쓰는 물건"),
    ("지하철", "도시에서 빠르게 이동하는 교통수단"), ("우산", "비 올 때 사용하는 물건"),
    ("책상", "공부하거나 일할 때 쓰는 가구"), ("선풍기", "바람을 일으키는 전자기기"),
    ("김밥", "밥과 재료를 말아 만든 음식"), ("강아지", "멍멍 짖는 반려동물"),
    ("고양이", "야옹하는 반려동물"), ("연필", "글씨 쓰는 도구"),
    ("이불", "자고 덮는 침구"), ("베개", "머리를 받치는 물건"),
    ("우물 안 개구리", "세상 물정을 모르는 사람"), ("하늘의 별 따기", "매우 어려운 일"),
    ("호랑이도 제 말하면 온다", "누구 이야기하면 나타난다"),
    ("가는 말이 고와야 오는 말이 곱다", "예의는 서로 지켜야 한다"),
    ("백문이 불여일견", "백 번 듣는 것보다 한 번 보는 게 낫다"),
    ("믿는 도끼에 발등 찍힌다", "믿던 사람에게 배신당함"),
    ("돌다리도 두들겨 보고 건너라", "확실한 것도 확인하라"),
    ("고래 싸움에 새우 등 터진다", "강자 싸움에 약자가 피해봄"),
    ("티끌 모아 태산", "작은 것도 모이면 커짐"), ("공든 탑이 무너지랴", "정성 들인 일은 헛되지 않음"),
    ("낮말은 새가 듣고 밤말은 쥐가 듣는다", "항상 말조심 하라"),
    ("우유", "흰색 액체 음료"), ("휴대폰", "통화나 메시지를 보낼 수 있는 기기"),
    ("수건", "물기 닦는 천"), ("삼겹살", "구워먹는 돼지고기"),
    ("김치찌개", "김치로 만든 찌개"), ("된장국", "된장으로 끓인 국"),
    ("감자", "뿌리 채소의 일종")
]

# 세션 상태 초기화
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
    st.session_state.answer_input = ""

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
            st.session_state.start_time = time.time()
            st.session_state.problem_start_time = time.time()
            st.session_state.score = 0
            st.session_state.show_hint = False
            st.session_state.started = True
            st.rerun()

# 게임 진행
elif not st.session_state.game_over:
    now = time.time()
    elapsed = now - st.session_state.start_time
    remaining = LIMIT_TIME - elapsed

    if remaining <= 0:
        st.session_state.game_over = True
        st.rerun()

    # 색상 전환
    color = "green" if remaining > 30 else "orange" if remaining > 15 else "red"
    st.markdown(f"<h4 style='color:{color}'>⏱ 남은 시간: {int(remaining)}초</h4>", unsafe_allow_html=True)
    st.markdown(f"🏆 현재 점수: **{st.session_state.score}개**")

    initials = get_initials(st.session_state.current_word)
    st.markdown(f"### 🔤 초성: **{initials}**")

    # 입력창 및 힌트
    answer = st.text_input("정답 입력:", value=st.session_state.answer_input, key="answer_box")

    if not st.session_state.show_hint and now - st.session_state.problem_start_time >= 3:
        st.session_state.show_hint = True

    if st.session_state.show_hint:
        st.markdown(f"<div style='color:gray; margin-top:-8px;'>💡 힌트: {st.session_state.hint}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    if col1.button("제출"):
        if answer.strip() == st.session_state.current_word:
            st.success("🎉 정답입니다!")
            st.session_state.score += 1
        else:
            st.warning("❌ 오답입니다. 다음 문제로 넘어갑니다.")

        # 다음 문제
        if not st.session_state.word_list:
            st.session_state.word_list = WORDS.copy()
            random.shuffle(st.session_state.word_list)

        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.session_state.answer_input = ""  # 입력창 초기화
        st.rerun()

    if col2.button("패스"):
        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.session_state.answer_input = ""
        st.rerun()

# 게임 종료 및 랭킹 저장
else:
    st.title("🏁 게임 종료!")
    st.markdown(f"**{st.session_state.name}**님의 점수는 **{st.session_state.score}점**입니다.")

    # 기존 데이터 불러오기
    if os.path.exists(SCORE_FILE):
        df = pd.read_csv(SCORE_FILE)
        df = df[df["이름"] != st.session_state.name]  # 기존 이름 제거
    else:
        df = pd.DataFrame(columns=["이름", "점수"])

    # 현재 점수 추가
    new_data = pd.DataFrame([{"이름": st.session_state.name, "점수": st.session_state.score}])
    df = pd.concat([df, new_data], ignore_index=True)
    df = df.sort_values(by="점수", ascending=False).reset_index(drop=True)
    df.to_csv(SCORE_FILE, index=False)

    st.markdown("## 🏆 현재 랭킹 (중복 없이)")
    st.dataframe(df.head(10))

    if st.button("🔁 다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
