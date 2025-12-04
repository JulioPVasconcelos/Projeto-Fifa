import streamlit as st
import requests
import base64


st.set_page_config(page_title="Clubes", page_icon="⚽", layout="wide")

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

df_filtered = df_data[df_data["Club"] == club].set_index("Name")

st.image(preprocess_row(df_filtered.iloc[0]["Club Logo"]))
st.markdown(f"## {club}")

columns = ["Age", "Overall", "Value(£)", "Wage(£)", "Joined", "Height", "Contract Valid Until", "Release Clause(£)"]

st.dataframe(df_filtered[columns], column_config={
    "Overall": st.column_config.ProgressColumn("Overall", format="%d",  min_value=0, max_value=100),
    "Wage(£)": st.column_config.ProgressColumn("Salário Semanal", format="%f",  min_value=0, max_value=df_filtered["Wage(£)"].max()),
    "Height": st.column_config.NumberColumn("Altura (cm)", format="%d cm"),
    "Release Clause(£)": st.column_config.ProgressColumn("Cláusula de Recisão", format="%f",  min_value=0, max_value=df_filtered["Release Clause(£)"].max())
})