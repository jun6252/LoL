# 파일명: app.py
import streamlit as st
import random
import time
import pandas as pd
import os

SCORE_FILE = "scores.csv"
LIMIT_TIME = 45  # 제한 시간 45초

# 초성 추출 함수
def get_initials(word):
    CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    initials = ""
    for char in word:
        if '가' <= char <= '힣':
            code = ord(char) - ord('가')
            cho = code // 588
            initials += CHOSUNG_LIST[cho]
        else:
            initials += char
    return initials

# 제시어 (진짜 한국어 단어 + 속담만, 줄임말/영어 제거)
WORDS = [
    ("냉장고", "음식을 차갑게 보관하는 기기"), ("지하철", "도시에서 이용하는 대중교통"),
    ("치약", "이를 닦을 때 사용하는 물건"), ("우산", "비 올 때 사용하는 물건"),
    ("컴퓨터", "문서 작업이나 코딩에 쓰는 기기"), ("책상", "공부하거나 일할 때 쓰는 가구"),
    ("선풍기", "더운 날 사용하는 바람 기계"), ("김밥", "밥과 재료를 말아서 만든 음식"),
    ("강아지", "멍멍 짖는 반려동물"), ("고양이", "야옹하는 반려동물"),
    ("전화기", "통화할 수 있는 기기"), ("빵", "밀가루로 만든 간식"),
    ("삼겹살", "구워 먹는 돼지고기"), ("김치찌개", "김치 넣고 끓인 찌개"),
    ("연필", "글씨 쓰는 도구"), ("이불", "잘 때 덮는 것"),
    ("된장국", "된장으로 끓인 국"), ("베개", "머리 받치는 침구"),
    ("감자", "전으로도 먹는 뿌리채소"), ("수건", "물기 닦는 천"),
    # 속담 25개
    ("등잔 밑이 어둡다", "가까운 것을 더 모른다"), ("하늘의 별 따기", "매우 어려운 일"),
    ("백문이 불여일견", "백 번 듣는 것보다 한 번 보는 게 낫다"),
    ("가는 말이 고와야 오는 말이 곱다", "예의는 서로 지켜야 한다"),
    ("호랑이도 제 말하면 온다", "누구 이야기하면 나타난다"),
    ("티끌 모아 태산", "작은 것도 모이면 커진다"),
    ("고래 싸움에 새우 등 터진다", "강자 싸움에 약자가 피해본다"),
    ("믿는 도끼에 발등 찍힌다", "믿은 사람에게 배신당함"),
    ("돌다리도 두들겨 보고 건너라", "확실한 것도 확인해야 한다"),
    ("낮말은 새가 듣고 밤말은 쥐가 듣는다", "항상 말조심 하라"),
    ("우물 안 개구리", "세상 물정을 모르는 사람"),
    ("빈 수레가 요란하다", "실속 없는 사람이 더 떠든다"),
    ("열 번 찍어 안 넘어가는 나무 없다", "노력하면 된다"),
    ("누워서 침 뱉기", "자기 자신에게 해가 되는 행동"),
    ("가는 날이 장날이다", "뜻하지 않은 상황을 만남"),
    ("눈에 넣어도 아프지 않다", "매우 귀엽고 사랑스럽다"),
    ("하룻강아지 범 무서운 줄 모른다", "무식한 자가 용감하다"),
    ("개천에서 용 난다", "미천한 출신에서 훌륭한 인물이 남"),
    ("고생 끝에 낙이 온다", "고생 후에 즐거움이 온다"),
    ("비 온 뒤에 땅이 굳는다", "시련 뒤 더 단단해짐"),
    ("바늘 도둑이 소 도둑 된다", "작은 잘못이 큰 죄가 된다"),
    ("공든 탑이 무너지랴", "정성 들인 일은 헛되지 않는다"),
    ("뛰는 놈 위에 나는 놈 있다", "항상 더 뛰어난 사람이 있다"),
    ("늦게 배운 도둑이 날 새는 줄 모른다", "늦게 배운 것에 빠짐"),
    ("호미로 막을 걸 가래로 막는다", "작은 문제도 빨리 해결해야 한다")
]

# 초기화
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
    st.title("🧠 문제를 맞혀보세요!")

    now = time.time()
    elapsed = now - st.session_state.start_time
    remaining = LIMIT_TIME - elapsed

    if remaining <= 0:
        st.session_state.game_over = True
        st.rerun()

    st.markdown(f"⏱ 남은 시간: **{int(remaining)}초**")
    st.markdown(f"🏆 점수: **{st.session_state.score}개**")

    word = st.session_state.current_word
    hint = st.session_state.hint
    initials = get_initials(word)

    st.markdown(f"### 🔤 초성: **{initials}**")
    answer = st.text_input("정답을 입력하세요:")

    if not st.session_state.show_hint and now - st.session_state.problem_start_time >= 3:
        st.session_state.show_hint = True

    # 힌트: 입력칸 아래, 고정 위치
    if st.session_state.show_hint:
        st.markdown(f"<div style='margin-top:-10px; color: gray;'>💡 힌트: {hint}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("제출"):
        if answer.strip() == word:
            st.success("🎉 정답입니다!")
            st.session_state.score += 1
        else:
            st.warning("❌ 틀렸지만 다음 문제로 넘어갑니다.")

        if not st.session_state.word_list:
            st.session_state.word_list = WORDS.copy()
            random.shuffle(st.session_state.word_list)

        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.rerun()

    if col2.button("패스"):
        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.rerun()

# 게임 종료
else:
    st.title("🏁 게임 종료!")
    st.markdown(f"**{st.session_state.name}** 님의 점수는 **{st.session_state.score}점**입니다!")

    new_data = pd.DataFrame([{"이름": st.session_state.name, "점수": st.session_state.score}])

    if os.path.exists(SCORE_FILE):
        old_data = pd.read_csv(SCORE_FILE)
        df = pd.concat([old_data, new_data], ignore_index=True)
    else:
        df = new_data

    df = df.sort_values(by="점수", ascending=False).reset_index(drop=True)
    df.to_csv(SCORE_FILE, index=False)

    st.markdown("## 🏆 랭킹")
    st.dataframe(df.head(10))

    if st.button("다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
