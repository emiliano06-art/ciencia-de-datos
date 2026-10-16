import streamlit as st
import pandas as pd


st.set_page_config(page_title="Uso de bicicletas", layout="wide")


st.title("Uso de bicicletas")


DATA_URL = "https://raw.githubusercontent.com/adsoftsito/nosql/refs/heads/main/csv/citibike-tripdata.csv"


@st.cache_data
def cargar_datos(url):
    data = pd.read_csv(url)
    
    if 'started_at' in data.columns:
        data['started_at'] = pd.to_datetime(data['started_at'], errors='coerce')
    if 'ended_at' in data.columns:
        data['ended_at'] = pd.to_datetime(data['ended_at'], errors='coerce')
    return data


try:
    df = cargar_datos(DATA_URL)
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    df = pd.DataFrame()


st.sidebar.title("Configuración")
mostrar_raw = st.sidebar.checkbox("View RAW data")
mostrar_horas = st.sidebar.checkbox("Recorridos por hora")
mostrar_mapa = st.sidebar.checkbox("Mapa")

if not df.empty:
    if mostrar_raw:
        st.subheader("Datos RAW (Crudos)")
        st.dataframe(df)
    else:
        st.subheader("Vista general del uso de bicicletas")
        st.dataframe(df.head(10))

    if mostrar_horas and 'started_at' in df.columns:
        st.subheader("Recorridos por hora")
        df['hora'] = df['started_at'].dt.hour
        conteo_horas = df['hora'].value_counts().sort_index()
        st.bar_chart(conteo_horas)


    if mostrar_mapa:
        if 'start_lat' in df.columns and 'start_lng' in df.columns:
            st.subheader("Mapa de ubicaciones de inicio")
            mapa_df = df[['start_lat', 'start_lng']].dropna().rename(columns={'start_lat': 'lat', 'start_lng': 'lon'})
            st.map(mapa_df)
        else:
            st.warning("El archivo CSV no contiene columnas de latitud ('start_lat') y longitud ('start_lng') para mostrar el mapa.")
else:
    st.warning("No hay datos disponibles para mostrar.")


st.markdown("---")
st.header("Integrantes del equipo")
st.markdown("### Emiliano Rico Borbonio")
st.markdown("### Isaac Becerril Carrera")