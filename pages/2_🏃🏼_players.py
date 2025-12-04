import streamlit as st
import requests
import base64

st.set_page_config(page_title="Jogadores", page_icon="🏃🏽‍♂️", layout="wide")

@st.cache_data
def url_to_base64_cached(url):
  headers = {
    "User-Agent": "Mozilla/5.0"
  }
  data = requests.get(url, headers=headers).content
  return "data:image/png;base64," + base64.b64encode(data).decode()

def preprocess_row(url):
  if isinstance(url, str) and url.startswith("http"):
    return url_to_base64_cached(url)
  return url

df_data = st.session_state["data"]

clubes = df_data["Club"].unique()
club = st.sidebar.selectbox("Clube", clubes)

df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].unique()
player = st.sidebar.selectbox("Jogador", players)

df_filtered = df_data[(df_data["Club"] == club)].set_index("Name")

# ADICIONADO --------------------------------------------------
df_filtered["Photo"] = df_filtered["Photo"].apply(preprocess_row)
df_filtered["Flag"] = df_filtered["Flag"].apply(preprocess_row)
df_filtered["Club Logo"] = df_filtered["Club Logo"].apply(preprocess_row)

player_stats = df_filtered.loc[player]

st.image(player_stats.Photo)
st.title(player_stats.name)

st.markdown(f"**Clube:** {player_stats.Club}")
st.markdown(f"**Posição:** {player_stats.Position}")


col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"**Idade:** {player_stats.Age}")
col2.markdown(f"**Altura:** {player_stats.Height / 100} cm")
col3.markdown(f"**Peso:** {player_stats.Weight * 0.453592:.2f} kg")
st.divider()

st.subheader(f"Overall: {player_stats.Overall}")
st.progress(int(player_stats.Overall))

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Valor de Mercado", value=f"£{player_stats['Value(£)']:,}")
col2.metric(label="Salário Semanal", value=f"£{player_stats['Wage(£)']:,}")
col3.metric(label="Cláusula de recisão", value=f"£{player_stats['Release Clause(£)']:,}")