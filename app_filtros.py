import streamlit as st
import pandas as pd
import plotly.express as px

# Dados de exemplo
df = pd.DataFrame({
    "Mês": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
    "Vendas": [120, 145, 98, 200, 175, 230],
    "Clientes": [40, 55, 35, 80, 70, 95],
})

# Cabeçalho
st.title("Painel de Vendas")
st.write("Resumo dos últimos 6 meses")

# Exibe o dataframe
st.subheader("Dados brutos")
st.dataframe(df, use_container_width=True)

#Aplica o select box para filtrar por mês
mes = st.selectbox("Mês",df["Mês"].unique())
# Mostar o dataframe filtrado
df_filtrado = df[df["Mês"] == mes]
# Exibe o dataframe filtrado
st.dataframe(df_filtrado)

# Plota o gráfico de barras com os dados filtrados
st.subheader("Vendas por mês")
fig_bar = px.bar(df_filtrado, x="Mês", y="Vendas", text="Vendas")
st.plotly_chart(fig_bar, use_container_width=True)

# Cria um slider — retorna um número
minimo = st.slider(
    "Vendas mínimas",
    min_value=0,
    max_value=230,
    value=100   # valor inicial
)

# Usa o valor para filtrar o DataFrame
filtrado = df[df["Vendas"] >= minimo]
st.dataframe(filtrado)

# Plota o gráfico de barras com os dados filtrados do slider
st.subheader("Vendas por mês - Filtro Slider")
fig_bar_slider = px.bar(filtrado, x="Mês", y="Vendas", text="Vendas")
st.plotly_chart(fig_bar_slider, use_container_width=True)

# Retorna uma LISTA com os selecionados
meses = st.multiselect(
    "Selecione os meses",
    options=df["Mês"].tolist(),
    default=["Jan", "Fev"]  # pré-selecionados
)

# .isin() filtra as linhas da lista
if meses:  # só filtra se tiver algo selecionado
    filtrado = df[df["Mês"].isin(meses)]
    st.dataframe(filtrado)
else:
    st.warning("Selecione ao menos um mês.")

# Gráfico de barras com Plotly
st.subheader("Vendas por mês - Filtro Múltiplo")
fig_bar = px.bar(filtrado, x="Mês", y="Vendas", text="Vendas")
st.plotly_chart(fig_bar, use_container_width=True)



