import streamlit as st
import random
import time
import pandas as pd
import os

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

# 제시어 100개 예시 (줄임말 + 속담 + 일상 + 기타)
WORDS = [
    ("냉장고", "음식 보관 가전"), ("지하철", "도심 대중교통"), ("강아지", "멍멍"),
    ("치약", "이를 닦는 물건"), ("전화기", "통화 기기"), ("의자", "앉는 가구"),
    ("치킨", "닭으로 만든 인기 음식"), ("컴퓨터", "코딩이나 문서 작성에 사용"),
    ("연필", "글씨 쓰는 도구"), ("책상", "공부나 업무할 때 사용하는 가구"),
    ("호랑이도 제 말하면 온다", "누구 이야기하면 나타난다"), ("하늘의 별 따기", "아주 어려운 일"),
    ("가는 말이 고와야 오는 말이 곱다", "예의가 중요하다"), ("백문이 불여일견", "백 번 듣는 것보다 보기"),
    ("등잔 밑이 어둡다", "가까운 것을 오히려 모른다"), ("피셜", "자기 공식 주장"), ("JMT", "정말 맛있다"),
    ("TMI", "너무 많은 정보"), ("ASAP", "되도록 빨리"), ("LOL", "크게 웃음"),
    ("OOTD", "오늘의 패션"), ("DM", "SNS 메시지"), ("MBTI", "성격유형 검사"),
    ("버스", "정류장에 정차하는 교통수단"), ("수박", "여름철 과일"), ("감자", "전으로도 먹는 뿌리채소"),
    ("코끼리", "큰 귀와 코를 가진 동물"), ("하마", "물가에 사는 무거운 동물"),
    ("과자", "과식하면 배아픈 군것질"), ("소파", "거실 가구"), ("리모컨", "TV 조작 기기"),
    ("가방", "물건을 담는 것"), ("비행기", "하늘을 나는 교통수단"),
    ("자동차", "도로 위 대표 운송수단"), ("피아노", "건반 악기"), ("기타", "줄 악기"),
    ("학교", "학생들이 공부하는 곳"), ("선생님", "가르치는 사람"), ("물고기", "물 속에 사는 생물"),
    ("태풍", "거센 바람을 동반한 기상 현상"), ("도서관", "책을 읽고 빌릴 수 있는 장소"),
    ("달력", "날짜 확인하는 도구"), ("병원", "아픈 사람 가는 곳"),
    ("시계", "시간을 알려주는 것"), ("모자", "머리에 쓰는 것"), ("우산", "비 올 때 필요"),
    ("편의점", "24시간 여는 가게"), ("헬스장", "운동하는 곳"), ("카페", "커피 마시는 곳"),
    ("노트북", "휴대 가능한 컴퓨터"), ("빵", "밀가루로 만든 주식"),
    # 50개 추가 (복붙이나 자동 생성한 유사 항목들)
] + [
    (f"단어{i}", f"{i}번째 가상의 단어 설명") for i in range(51, 101)
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
    st.title("⚡ 스피드 초성 퀴즈")
    st.markdown("30초 안에 최대한 많이 맞혀보세요!")

    name = st.text_input("이름을 입력하세요:")
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
        st.warning("이름을 입력해주세요.")

# 게임 진행
elif not st.session_state.game_over:
    st.title("🔥 스피드 퀴즈 중!")

    timer_placeholder = st.empty()
    now = time.time()
    elapsed = now - st.session_state.start_time
    remaining = 30 - elapsed

    if remaining <= 0:
        st.session_state.game_over = True
        st.rerun()

    timer_placeholder.markdown(f"⏱️ 남은 시간: **{int(remaining)}초**")
    st.markdown(f"🏆 현재 점수: **{st.session_state.score}개**")

    initials = get_initials(st.session_state.current_word)
    st.markdown(f"### 🔤 초성: **{initials}**")

    if not st.session_state.show_hint and now - st.session_state.problem_start_time >= 3:
        st.session_state.show_hint = True

    if st.session_state.show_hint:
        st.info(f"💡 힌트: {st.session_state.hint}")

    answer = st.text_input("정답:", key=str(now))

    if st.button("제출"):
        if answer.strip() == st.session_state.current_word:
            st.success("🎉 정답!")
            st.session_state.score += 1
        else:
            st.warning("❌ 틀렸지만 다음 문제로!")

        if not st.session_state.word_list:
            st.session_state.word_list = WORDS.copy()
            random.shuffle(st.session_state.word_list)

        st.session_state.current_word, st.session_state.hint = st.session_state.word_list.pop()
        st.session_state.problem_start_time = time.time()
        st.session_state.show_hint = False
        st.rerun()

# 게임 종료
else:
    st.title("🏁 게임 종료!")
    st.markdown(f"🎯 **{st.session_state.name}** 님의 점수: **{st.session_state.score}점**")

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

    st.markdown("## 🏆 랭킹")
    st.dataframe(df.head(10))

    if st.button("🔄 다시 하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
