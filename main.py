import streamlit as st

st.set_page_config(page_title="LoL 라인별 추천 챔피언", layout="centered")

st.title("🎮 리그 오브 레전드 라인별 추천 챔피언")
st.markdown("게임을 처음 시작하셨나요? 라인을 선택하면 해당 라인에서 자주 사용되는 챔피언들을 추천해드릴게요!")

# 라인별 챔피언 데이터
champions_by_role = {
    "탑 (Top)": [
        "Aatrox", "Camille", "Cho'Gath", "Darius", "Dr. Mundo", "Fiora", "Garen",
        "Gnar", "Gragas", "Illaoi", "Jax", "Malphite", "Mordekaiser", "Nasus",
        "Ornn", "Pantheon", "Sett", "Shen", "Singed", "Sion", "Teemo", "Urgot",
        "Volibear", "Yone", "Yorick"
    ],
    "정글 (Jungle)": [
        "Amumu", "Bel'Veth", "Briar", "Diana", "Ekko", "Elise", "Evelynn", "Fiddlesticks",
        "Graves", "Hecarim", "Jarvan IV", "Karthus", "Kayn", "Kha'Zix", "Kindred",
        "Lee Sin", "Lillia", "Master Yi", "Nidalee", "Nocturne", "Nunu", "Rammus",
        "Rek'Sai", "Rengar", "Sejuani", "Shaco", "Trundle", "Vi", "Viego", "Warwick", "Wukong", "Zac"
    ],
    "미드 (Mid)": [
        "Ahri", "Akali", "Anivia", "Annie", "Azir", "Brand", "Cassiopeia", "Diana",
        "Ekko", "Fizz", "Galio", "Heimerdinger", "Irelia", "Kassadin", "Katarina",
        "LeBlanc", "Lissandra", "Lux", "Malzahar", "Neeko", "Orianna", "Qiyana",
        "Ryze", "Sylas", "Syndra", "Talon", "Twisted Fate", "Veigar", "Vex", "Viktor",
        "Vladimir", "Xerath", "Yasuo", "Yone", "Zed", "Ziggs", "Zoe"
    ],
    "원딜 (Bot/ADC)": [
        "Aphelios", "Ashe", "Caitlyn", "Draven", "Ezreal", "Jhin", "Jinx", "Kai'Sa",
        "Kalista", "Kog'Maw", "Lucian", "Miss Fortune", "Nilah", "Samira", "Sivir",
        "Smolder", "Tristana", "Twitch", "Varus", "Vayne", "Xayah", "Zeri"
    ],
    "서포트 (Support)": [
        "Alistar", "Bard", "Blitzcrank", "Brand", "Braum", "Janna", "Karma", "Leona",
        "Lulu", "Lux", "Milio", "Morgana", "Nami", "Nautilus", "Neeko", "Pantheon",
        "Pyke", "Rakan", "Rell", "Renata Glasc", "Senna", "Seraphine", "Sona", "Soraka",
        "Swain", "Taric", "Thresh", "Vel'Koz", "Xerath", "Yuumi", "Zilean", "Zyra"
    ]
}

# 사용자 입력
selected_role = st.selectbox("라인을 선택하세요", list(champions_by_role.keys()))

# 결과 출력
if selected_role:
    st.subheader(f"🧾 {selected_role} 추천 챔피언 리스트")
    st.markdown(
        ", ".join(champions_by_role[selected_role])
    )
    st.success("선택한 라인에 맞는 챔피언들을 연습해보세요!")

# 부가 정보
st.markdown("---")
st.caption("📌 챔피언에 따라 난이도와 스타일이 다를 수 있어요. 초보자에게는 탱키하고 조작이 쉬운 챔피언부터 추천합니다.")

