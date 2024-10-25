import streamlit as st
import pandas as pd
import plotly.express as px


# Função para carregar dados do Google Sheets sem autenticação
def carregar_dados():
    # URL da planilha pública do Google Sheets em formato CSV
    sheet_url = "https://docs.google.com/spreadsheets/d/1rFGMKTSaYRueLlYzygnTLXMehujlNoRokW1ehfHF7IA/gviz/tq?tqx=out:csv&gid=0"

    # Carregar os dados para um DataFrame do pandas
    df = pd.read_csv(sheet_url)
    return df

# Função principal do Streamlit
def main():
    # Aplicar estilo ao título
    st.markdown(
        """
        <h1 style='text-align: center; background-color: purple; border-radius: 10px; padding: 10px; color: white;'>
        Sunrise Nordeste Brasil
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.write(" ")
    
    # Carregar dados do Google Sheets
    df = carregar_dados()

    # Sidebar para os filtros
    st.sidebar.header("Filtros")
    
    sexo = st.sidebar.multiselect("Sexo", options=df["Sexo"].unique(), default=df["Sexo"].unique())
    creche = st.sidebar.multiselect("Código da Creche", options=df["Código da Creche"].unique(), default=df["Código da Creche"].unique())
    questionario = st.sidebar.selectbox("Questionário", ["SIM", "NAO"])
    avaliacao = st.sidebar.selectbox("Testes", ["SIM", "NAO"])

    # Aplicar os filtros
    df_filtrado = df[(df["Sexo"].isin(sexo)) & 
                     (df["Código da Creche"].isin(creche)) & 
                     (df["Questionário"] == questionario) & 
                     (df["Testes"] == avaliacao)]

    # Se ainda não há dados filtrados, evita erro
    if not df_filtrado.empty:
    
        # Contar a quantidade de crianças por dias de uso
        df_dias_count = df_filtrado['Dias de uso'].value_counts().reset_index()
        df_dias_count.columns = ['Dias de uso', 'Quantidade de indivíduos']  
        
        # Criar gráfico de barras
        fig_barras = px.bar(df_dias_count, 
                            x='Dias de uso', 
                            y='Quantidade de indivíduos',
                            title="Quantidade de indivíduos por Dias de Uso",
                            labels={'Dias de uso': 'Dias de Uso', 'Quantidade de indivíduos': 'Quantidade de indivíduos'},
                            color_discrete_sequence=['orange', 'purple'])
        
        st.write(" ")

        # Centralizar o título do gráfico
        fig_barras.update_layout(title_x=0.3)  
        st.plotly_chart(fig_barras)

        # Gráfico de pizza para distribuição da idade por dias de uso
        fig_pizza = px.pie(df_filtrado, names='Idade', values='Dias de uso', 
                           title="Distribuição de Idade por Dias de Uso",
                           color_discrete_sequence=['orange', 'purple'])
        
        # Centralizar o título do gráfico
        fig_pizza.update_layout(title_x=0.25)  
        st.plotly_chart(fig_pizza)

    else:
        st.write("Nenhum dado correspondente aos filtros selecionados.")

# Executar a aplicação Streamlit
if __name__ == "__main__":
    main()
