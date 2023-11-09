import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv("acidentes2022.csv", on_bad_lines="skip", sep=";")

# tratamento de dad

df["vitimasfatais"] = df["vitimasfatais"].str.replace(",", ".").astype(float)
df["vitimas"] = df["vitimas"].str.replace(",", ".").astype(float)

#total de acidentes por clima
clima = df["tempo_clima"].value_counts().sort_values(ascending=False)

#total de acientes por bairro
bairro = df["bairro"].value_counts().head(10).sort_values(ascending=True)

# alterando coluna de data para datetime
df["data"] = pd.to_datetime(df["data"])

# Criando coluna de mês
df["Mês_Acidente"] = df["data"].dt.month

total_mes = df["Mês_Acidente"].value_counts().reset_index()
total_mes = total_mes.sort_values(by="Mês_Acidente")


def main():
    st.image("./logo_gestao_pcr_alt_horizontal.png")
    st.header("Acidentes de trânsito em Recife - 2022")

    total_acidentes = df.shape[0]
    total_vitimas = df["vitimas"].sum()
    total_vitimas_fatais = df["vitimasfatais"].sum()


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Acidentes 🚨", total_acidentes)

    with col2:
        st.metric("Total Vítimas 🤕", total_vitimas)

    with col3:
        st.metric("Total Vítimas Fatais ⚰️", total_vitimas_fatais)

    fig = px.bar(clima, text=clima.values, color_discrete_sequence=["#FF4500"])
    fig.update_layout(title="Total de acidentes por Clima", title_x=0.3, showlegend=False)
    st.plotly_chart(fig)
   
    fig1 = px.bar(bairro, text=bairro.values, color_discrete_sequence=["#FF4500"], orientation="h")
    fig1.update_layout(title="Top 10 acidentes por Bairro", title_x=0.3,showlegend=False)
    st.plotly_chart(fig1)
    
    fig2 = px.line(total_mes, x="Mês_Acidente", y="count",
              color_discrete_sequence=["#FF4500"], markers=True,
              text="count", labels={"Mês":"Mês Acidente", "Total":"Total Acidentes"})
    fig2.update_layout(title='Total de acidentes por mês', title_x=0.3)
    fig2.update_traces(textposition='top center')
    st.plotly_chart(fig2)
    
if __name__ == "__main__":
    main()
