import streamlit as st
import pandas as pd 
import plotly.express as px 

from streamlit_option_menu  import option_menu
from numerize.numerize import numerize

#llamar query.py
from query import *


st.set_page_config(page_title="Dashboard SSO", page_icon="🌐",layout="wide")
st.subheader("📊 Análisis Mercado Público")
st.markdown("Una mirada transversal del proceso de compra")


#Consulta Data
result = view_all_data()
df = pd.DataFrame(result, columns=[
    "Policy",
    "Expiry",
    "Location",
    "State",
    "Region",
    "Investment",
    "Construction",
    "BusinessType",
    "Earthquake",
    "Flood",
    "Rating",
    "id"
])

#Mostrar Información
#st.dataframe(df)

#Barra Lateral
st.sidebar.image("data/logoSSO.png", caption="Servicio Salud de Osorno", width=250)

#Filtros
st.sidebar.header("Aplicar Filtro")
region=st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique(),
)

location=st.sidebar.multiselect(
    "Select Location",
    options=df["Location"].unique(),
    default=df["Location"].unique(),
)

construction=st.sidebar.multiselect(
    "Select Construction",
    options=df["Construction"].unique(),
    default=df["Construction"].unique(),
)

df_selection=df.query(
    "Region==@region & Location==@location & Construction==@construction"
)



def Home():
    with st.expander("Tabular"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=[])
        st.write(df_selection[showData])
    
    # Compute top analytics
    total_investment = df_selection['Investment'].sum()
    investment_mode = df_selection['Investment'].mode().iloc[0] if not df_selection.empty else 0  # Moda de la inversión
    investment_mean = df_selection['Investment'].mean() if not df_selection.empty else 0
    investment_median = df_selection['Investment'].median() if not df_selection.empty else 0
    rating = df_selection['Rating'].sum() if not df_selection.empty else 0
    
    total1, total2, total3, total4, total5 = st.columns(5)
    with total1:
        st.info('Total Investment', icon="📌")
        st.metric(label="sum  TZS", value=f"{total_investment:,.0f}")

    with total2:
        st.info('Most Frequent', icon="📌")
        st.metric(label="mode  TZS", value=f"{investment_mode:,.0f}")
        
    with total3:
        st.info('Average', icon="📌")
        st.metric(label="average  TZS", value=f"{investment_mean:,.0f}")
        
    with total4:
        st.info('Central Earnings', icon="📌")
        st.metric(label="median  TZS", value=f"{investment_median:,.0f}")

    with total5:
        st.info('Ratings', icon="📌")
        st.metric(label="Rating", value=numerize(rating), help=f"Total Rating: {rating}")

    st.markdown("---")

#Graficos

def graphs():
    #total_investment=int(df_selection['Investment']).sum()
    #averageRating=int(round(df_selection['Rating']).mean(),2)
    
    
    # Gráfico de Barra
    investment_by_business_type = df_selection.groupby(by=['BusinessType']).count()[['Investment']].sort_values(by='Investment')
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="<b> Investment by Business type </b>",
        color_discrete_sequence=["#0083b8"] * len(investment_by_business_type),
        template="plotly_white"
    )

    # Actualizar gráfico de barra
    fig_investment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(title="Business Type")
    )

    # Gráfico de Línea
    investment_by_state = df_selection.groupby(by=['State']).count()[['Investment']]
    fig_state = px.bar(
        investment_by_state,
        x=investment_by_state.index,
        y="Investment",
        orientation="v",
        title="<b> Investment by State</b>",
        color_discrete_sequence=["#0083b8"] * len(investment_by_state),
        template="plotly_white"
    )

    # Actualizar gráfico de línea
    fig_state.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="State"),
        yaxis=dict(showgrid=False)
    )

    # Mostrar gráficos
    left, right = st.columns(2)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)

Home()
graphs()