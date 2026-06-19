
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Spotify Dashboard",
    page_icon="S",
    layout="wide"           
)

# -------------------------------------------------------------
# ESTILO VISUAL (CSS)
# Deixa o visual mais bonito com cores do Spotify
# -------------------------------------------------------------
st.markdown("""
    <style>
        /* Fundo geral da pagina */
        .stApp {
            background-color: #0f0f0f;
            color: #ffffff;
        }

        /* Titulo principal */
        h1 {
            color: #1DB954;
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -1px;
        }

        /* Subtitulos */
        h2, h3 {
            color: #ffffff;
        }

        /* Caixa dos KPIs (indicadores numericos) */
        .kpi-box {
            background: linear-gradient(135deg, #1a1a1a, #252525);
            border: 1px solid #1DB954;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }

        /* Numero do KPI */
        .kpi-number {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1DB954;
        }

        /* Rotulo do KPI */
        .kpi-label {
            font-size: 0.9rem;
            color: #b3b3b3;
            margin-top: 4px;
        }

        /* Linha separadora */
        hr {
            border-color: #1DB954;
            opacity: 0.3;
        }
    </style>
""", unsafe_allow_html=True)


# =============================================================
# CARREGAMENTO DOS DADOS
# =============================================================

# URL do arquivo CSV no GitHub
URL_DADOS = "https://raw.githubusercontent.com/Demibolt007/Spotify-Streaming-Insights-2010-2019/refs/heads/main/Spotify%20Dataset.csv"

# Le o CSV diretamente da internet e salva na variavel df
df = pd.read_csv(URL_DADOS)

# Remove linhas onde a coluna Streams esta vazia
df = df.dropna(subset=["Streams"])

# Garante que Streams e um numero inteiro
df["Streams"] = pd.to_numeric(df["Streams"], errors="coerce")
df = df.dropna(subset=["Streams"])
df["Streams"] = df["Streams"].astype(int)

# Garante que Year e um numero inteiro
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")


# =============================================================
# CABECALHO DO DASHBOARD
# =============================================================
st.markdown("# Spotify Streaming Dashboard")
st.markdown("**Explorando os dados de streaming do Spotify entre 2010 e 2019**")
st.markdown("---")


# =============================================================
# FILTROS INTERATIVOS (na barra lateral esquerda)
# -------------------------------------------------------------
# No Streamlit, tudo que começa com st.sidebar aparece
# na barra do lado esquerdo da tela.
#
# Filtro 1: Slider de ano   -> o usuario escolhe um intervalo
# Filtro 2: Multiselect     -> o usuario escolhe um ou mais generos
# =============================================================
st.sidebar.markdown("## Filtros")
st.sidebar.markdown("Use os filtros abaixo para explorar os dados:")

# FILTRO 1: Intervalo de anos
# sorted() ordena os anos do menor para o maior
anos_disponiveis = sorted(df["Year"].dropna().unique())

# int() converte para numero inteiro normal (o pandas usa Int64)
ano_min = int(min(anos_disponiveis))
ano_max = int(max(anos_disponiveis))

# st.sidebar.slider cria um controle deslizante com dois pontos
# value=(ano_min, ano_max) significa que começa mostrando todos os anos
intervalo_ano = st.sidebar.slider(
    "Ano de lancamento",
    min_value=ano_min,
    max_value=ano_max,
    value=(ano_min, ano_max)
)

# FILTRO 2: Genero musical
# sorted() ordena os generos em ordem alfabetica
generos_disponiveis = sorted(df["Genre"].dropna().unique())

# st.sidebar.multiselect cria uma lista onde o usuario pode
# marcar varios itens ao mesmo tempo
# default= define quais generos ja vem selecionados ao abrir
generos_escolhidos = st.sidebar.multiselect(
    "Genero musical",
    options=generos_disponiveis,
    default=generos_disponiveis[:8]     # começa com os 8 primeiros selecionados
)

# -------------------------------------------------------------
# APLICACAO DOS FILTROS
# -------------------------------------------------------------
# Aqui criamos um novo dataframe chamado df_filtrado
# que contem SOMENTE as linhas que passam pelos dois filtros.
#
# A condicao funciona assim:
#   (df["Year"] >= intervalo_ano[0])   -> ano maior ou igual ao minimo escolhido
#   (df["Year"] <= intervalo_ano[1])   -> ano menor ou igual ao maximo escolhido
#   (df["Genre"].isin(generos_escolhidos)) -> genero esta na lista selecionada
#
# O operador & significa "E" (todas as condicoes devem ser verdadeiras)
# -------------------------------------------------------------
df_filtrado = df[
    (df["Year"] >= intervalo_ano[0]) &
    (df["Year"] <= intervalo_ano[1]) &
    (df["Genre"].isin(generos_escolhidos))
]

# Mostra na barra lateral quantas musicas foram encontradas
st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(df_filtrado):,} musicas** encontradas com esses filtros.")


# =============================================================
# KPIs - INDICADORES NUMERICOS EM DESTAQUE
# Os KPIs sao calculados com base nos dados filtrados (df_filtrado)
# Entao eles mudam automaticamente quando o usuario mexe nos filtros
# =============================================================
st.markdown("### Indicadores Gerais")

col1, col2, col3 = st.columns(3)   # divide a linha em 3 colunas iguais

# KPI 1: Total de streams
total_streams = df_filtrado["Streams"].sum()
with col1:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-number">{total_streams / 1_000_000_000:.1f}B</div>
            <div class="kpi-label">Total de Streams</div>
        </div>
    """, unsafe_allow_html=True)

# KPI 2: Numero de musicas unicas
total_musicas = df_filtrado["Song"].nunique()
with col2:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-number">{total_musicas:,}</div>
            <div class="kpi-label">Musicas Unicas</div>
        </div>
    """, unsafe_allow_html=True)

# KPI 3: Media de BPM (batidas por minuto)
media_bpm = df_filtrado["Bpm"].mean()
with col3:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-number">{media_bpm:.0f}</div>
            <div class="kpi-label">BPM Medio</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")


# =============================================================
# GRAFICOS
# Todos os graficos usam df_filtrado, entao atualizam
# automaticamente quando o usuario muda um filtro.
# =============================================================

# --- GRAFICO 1 e 2: primeira linha ---
col_graf1, col_graf2 = st.columns(2)

# GRAFICO 1: Streams por ano (linha do tempo)
# Tipo: grafico de linha -> bom para mostrar tendencia ao longo do tempo
with col_graf1:
    st.markdown("#### Streams por Ano")

    # groupby("Year") agrupa todas as linhas pelo ano
    # ["Streams"].sum() soma os streams de cada grupo
    # reset_index() transforma o resultado em uma tabela normal
    streams_por_ano = (
        df_filtrado.groupby("Year")["Streams"]
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        streams_por_ano,
        x="Year",
        y="Streams",
        markers=True,                   # mostra pontinhos em cada ano
        color_discrete_sequence=["#1DB954"]
    )
    fig1.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        xaxis_title="Ano",
        yaxis_title="Total de Streams"
    )
    st.plotly_chart(fig1, use_container_width=True)

# GRAFICO 2: Top 10 artistas com mais streams
# Tipo: grafico de barras horizontal -> bom para comparar categorias com nomes longos
with col_graf2:
    st.markdown("#### Top 10 Artistas por Streams")

    top_artistas = (
        df_filtrado.groupby("Artist")["Streams"]
        .sum()
        .sort_values(ascending=True)    # crescente para o grafico horizontal ficar certo
        .tail(10)                       # pega os 10 maiores
        .reset_index()
    )

    fig2 = px.bar(
        top_artistas,
        x="Streams",
        y="Artist",
        orientation="h",                # "h" = horizontal
        color_discrete_sequence=["#1DB954"]
    )
    fig2.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        xaxis_title="Total de Streams",
        yaxis_title=""
    )
    st.plotly_chart(fig2, use_container_width=True)


# --- GRAFICO 3 e 4: segunda linha ---
col_graf3, col_graf4 = st.columns(2)

# GRAFICO 3: Distribuicao de generos musicais
# Tipo: grafico de pizza -> bom para mostrar proporcao entre categorias
with col_graf3:
    st.markdown("#### Streams por Genero Musical")

    streams_por_genero = (
        df_filtrado.groupby("Genre")["Streams"]
        .sum()
        .sort_values(ascending=False)
        .head(8)                        # mostra so os 8 principais generos
        .reset_index()
    )

    fig3 = px.pie(
        streams_por_genero,
        values="Streams",
        names="Genre",
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    fig3.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff"
    )
    st.plotly_chart(fig3, use_container_width=True)

# GRAFICO 4: Relacao entre Danceability e Streams
# Tipo: grafico de dispersao (scatter) -> bom para ver correlacao entre dois numeros
with col_graf4:
    st.markdown("#### Danceability vs. Streams")

    # min(500, len(df_filtrado)) garante que nao vai tentar pegar
    # mais pontos do que existem no dataframe filtrado
    fig4 = px.scatter(
        df_filtrado.sample(min(500, len(df_filtrado))),
        x="Danceability",
        y="Streams",
        color="Genre",
        opacity=0.7,
        hover_data=["Song", "Artist"],  # ao passar o mouse, mostra musica e artista
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig4.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        xaxis_title="Danceability (0-100)",
        yaxis_title="Streams"
    )
    st.plotly_chart(fig4, use_container_width=True)


# --- GRAFICO 5 e 6: terceira linha ---
col_graf5, col_graf6 = st.columns(2)

# GRAFICO 5: Distribuicao de BPM (histograma)
# Tipo: histograma -> bom para ver como os valores numericos se distribuem
with col_graf5:
    st.markdown("#### Distribuicao de BPM")

    fig5 = px.histogram(
        df_filtrado,
        x="Bpm",
        nbins=30,                       # divide em 30 faixas
        color_discrete_sequence=["#1DB954"]
    )
    fig5.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        xaxis_title="BPM (Batidas por Minuto)",
        yaxis_title="Quantidade de Musicas"
    )
    st.plotly_chart(fig5, use_container_width=True)

# GRAFICO 6: Energy vs Valence (humor da musica)
# Tipo: scatter com tamanho variavel -> mostra tres dimensoes ao mesmo tempo
with col_graf6:
    st.markdown("#### Energia vs. Positividade (Valence)")

    fig6 = px.scatter(
        df_filtrado.sample(min(500, len(df_filtrado))),
        x="Energy",
        y="Valence",
        size="Streams",                 # tamanho do ponto = quantidade de streams
        size_max=25,
        color="Year",
        hover_data=["Song", "Artist"],
        color_continuous_scale="Greens",
        opacity=0.8
    )
    fig6.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="#ffffff",
        xaxis_title="Energia (0-100)",
        yaxis_title="Positividade / Valence (0-100)"
    )
    st.plotly_chart(fig6, use_container_width=True)


# =============================================================
# TABELA DE DADOS
# Mostra as 10 musicas com mais streams no periodo filtrado
# =============================================================
st.markdown("---")
st.markdown("### Top 10 Musicas do Periodo Selecionado")

top_musicas = (
    df_filtrado[["Song", "Artist", "Genre", "Year", "Streams", "Popularity"]]
    .sort_values("Streams", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

# Faz o indice comecar em 1 ao inves de 0
top_musicas.index = top_musicas.index + 1

st.dataframe(
    top_musicas,
    use_container_width=True,
    column_config={
        "Streams": st.column_config.NumberColumn(format="%d")
    }
)

# =============================================================
# RODAPE
# =============================================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#b3b3b3; font-size:0.8rem;'>"
    "Dashboard criado com Python + Streamlit + Plotly | "
    "Dados: Spotify Streaming Insights 2010-2019"
    "</p>",
    unsafe_allow_html=True
)
