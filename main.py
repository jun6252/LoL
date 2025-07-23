import streamlit as st

st.set_page_config(page_title="LoL 챔피언 추천", layout="centered")
st.title("🎮 리그 오브 레전드 챔피언 추천 가이드")

st.markdown("게임 성향을 선택하면 라인에 맞는 챔피언을 더 정밀하게 추천해드려요!")

# ======== 1. 성향 검사 ========
st.header("1️⃣ 당신의 게임 성향은?")
style = st.radio("1. 팀에서 어떤 역할을 선호하나요?", ["앞에서 싸우는 탱커", "뒤에서 딜", "적을 교란", "아군 보호"])
difficulty = st.radio("2. 조작 난이도는?", ["쉬운 걸 선호", "어려워도 괜찮음"])
fight_type = st.radio("3. 어떤 전투를 선호하나요?", ["1:1 싸움", "집단전"])
mobility = st.radio("4. 빠르게 움직이면서 싸우는 건?", ["재밌다", "부담된다"])

# ======== 2. 라인 선택 ========
st.header("2️⃣ 라인을 선택하세요")
selected_role = st.selectbox("라인", ["탑 (Top)", "정글 (Jungle)", "미드 (Mid)", "원딜 (Bot/ADC)", "서포트 (Support)"])

# ======== 3. 챔피언 데이터 ========
champions_by_role_and_trait = {
    "미드 (Mid)": {
        "쉬운 딜러": ["Annie", "Malzahar", "Veigar"],
        "난이도 높고 민첩": ["Zed", "Yasuo", "Ekko"],
        "수비/광역 한타형": ["Orianna", "Viktor", "Lissandra"]
    },
    "정글 (Jungle)": {
        "쉬운 탱커": ["Amumu", "Rammus", "Zac"],
        "기동성과 교란": ["Lee Sin", "Kayn", "Rengar"],
        "광역 딜/싸움": ["Diana", "Fiddlesticks", "Graves"]
    },
    "탑 (Top)": {
        "쉬운 탱커": ["Garen", "Malphite", "Nasus"],
        "기동성/1:1강": ["Jax", "Camille", "Irelia"]
    },
    "원딜 (Bot/ADC)": {
        "쉬운 딜러": ["Miss Fortune", "Ashe", "Sivir"],
        "기동성 딜러": ["Ezreal", "Lucian", "Samira"]
    },
    "서포트 (Support)": {
        "힐/보호": ["Janna", "Soraka", "Lulu"],
        "이니시/탱커": ["Leona", "Nautilus", "Thresh"],
        "서폿딜/견제": ["Zyra", "Brand", "Xerath"]
    }
}

# ======== 4. 성향에 따른 태그 매핑 ========
def get_traits(style, difficulty, fight_type, mobility):
    traits = []

    if style == "앞에서 싸우는 탱커":
        traits.append("쉬운 탱커" if difficulty == "쉬운 걸 선호" else "이니시/탱커")
    elif style == "뒤에서 딜":
        traits.append("쉬운 딜러" if difficulty == "쉬운 걸 선호" else "기동성 딜러")
    elif style == "적을 교란":
        traits.append("기동성과 교란" if mobility == "재밌다" else "서폿딜/견제")
    elif style == "아군 보호":
        traits.append("힐/보호")

    if fight_type == "집단전":
        traits.append("수비/광역 한타형")
    elif fight_type == "1:1 싸움":
        traits.append("기동성/1:1강")

    return list(set(traits))  # 중복 제거

# ======== 5. 추천 챔피언 출력 ========
st.header("3️⃣ 추천 챔피언 🎯")

traits = get_traits(style, difficulty, fight_type, mobility)
recommended = []

if selected_role in champions_by_role_and_trait:
    role_data = champions_by_role_and_trait[selected_role]
    for t in traits:
        if t in role_data:
            recommended.extend(role_data[t])

if recommended:
    st.subheader(f"👉 당신에게 어울리는 챔피언 ({selected_role})")
    st.markdown(", ".join(set(recommended)))
    st.success("이 챔피언들부터 시작해보세요!")
else:
    st.warning("조건에 맞는 챔피언이 아직 등록되지 않았어요. 조건을 바꿔보세요!")

st.markdown("---")
st.caption("📌 해당 추천은 참고용이며, 실제 플레이 스타일과 궁합이 중요합니다!")
