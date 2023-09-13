# importar bibliotecas
import streamlit as st
import pandas as pd
import pydeck as pdk

#WideScreen a aplicação
st.set_page_config(page_title="App Análise de Acidentes Aeronáuticos", page_icon= "🛩", layout="wide")

#Load in preparation data
DATA_URL = "ocorrencias_aviacao.csv"

@st.cache_data
def load_data():
    """
    Carrega os dados de ocorrências aeronáuticas do CENIPA.

    :return: DataFrame com colunas selecionadas.
    """
    columns = {
        'ocorrencia_latitude': 'latitude',
        'ocorrencia_longitude': 'longitude',
        'ocorrencia_dia': 'data',
        'ocorrencia_classificacao': 'classificacao',
        'ocorrencia_tipo': 'tipo',
        'ocorrencia_tipo_categoria': 'tipo_categoria',
        'ocorrencia_tipo_icao': 'tipo_icao',
        'ocorrencia_aerodromo': 'aerodromo',
        'ocorrencia_cidade': 'cidade',
        'investigacao_status': 'status',
        'divulgacao_relatorio_numero': 'relatorio_numero',
        'total_aeronaves_envolvidas': 'aeronaves_envolvidas'
    }

    data = pd.read_csv(DATA_URL, index_col='codigo_ocorrencia')
    data = data.rename(columns=columns)
    data.data = data.data + " " + data.ocorrencia_horario
    data.data = pd.to_datetime(data.data)
    data = data[list(columns.values())]

    return data


df = load_data()
labels = df.classificacao.unique().tolist()


# SIDEBAR
# Parâmetros e número de ocorrências
st.sidebar.header("📌 Parâmetros")
info_sidebar = st.sidebar.empty()    # placeholder, para informações filtradas que só serão carregadas depois

# Slider de seleção do ano
st.sidebar.subheader("📅 Ano")
year_to_filter = st.sidebar.slider('Escolha o ano desejado', 2008, 2018)

# Checkbox da Tabela
st.sidebar.subheader("🗓 Tabela")
tabela = st.sidebar.empty()    # placeholder que só vai ser carregado com o df_filtered

# Multiselect com os lables únicos dos tipos de classificação
label_to_filter = st.sidebar.multiselect(
    label=" 🔎 Escolha a classificação da ocorrência",
    options=labels,
    default=["INCIDENTE", 'ACIDENTE']
)

# Informação no rodapé da Sidebar
st.sidebar.markdown("""
➡ A base de dados de ocorrências aeronáuticas é gerenciada pelo ***Centro de Investigação e Prevenção de Acidentes 
Aeronáuticos (CENIPA)***.
""")

# Somente aqui os dados filtrados por ano são atualizados em novo dataframe
filtered_df = df[(df.data.dt.year == year_to_filter) & (df.classificacao.isin(label_to_filter))]

# Aqui o placehoder vazio finalmente é atualizado com dados do filtered_df
info_sidebar.info("{} ocorrências selecionadas.".format(filtered_df.shape[0]))



# MAIN
st.markdown("<h2 style='text-align: center;'>📊 Análise de Acidentes Aeronáuticos </h2>", unsafe_allow_html=True)
st.info(f"""
            📍Estão sendo exibidas as ocorrências classificadas como **{", ".join(label_to_filter)}**
            para o ano de **{year_to_filter}**.
            """)

# raw data (tabela) dependente do checkbox
if tabela.checkbox("Mostrar tabela de dados"):
    st.write(filtered_df)


# mapa
st.subheader("Mapa de ocorrências")
st.map(filtered_df)

st.sidebar.divider()
st.sidebar.image("logo.png", width=300)