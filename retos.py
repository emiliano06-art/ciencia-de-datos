mport streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard en Producción",
    page_icon="📊",
    layout="wide"
)
@st.cache_data
def cargar_datos():
    data = {
        'ID': range(1, 101),
        'Categoria': ['Tecnología', 'Ropa', 'Alimentos', 'Tecnología', 'Ropa'] * 20,
        'Ciudad_Origen': ['Ciudad de México', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana'] * 20,
        'Ventas': [150, 200, 120, 300, 90, 400, 250, 110, 350, 180] * 10,
        'Satisfaccion': [4, 5, 3, 4, 5, 2, 4, 3, 5, 4] * 10
    }
    return pd.DataFrame(data)

df = cargar_datos()


st.sidebar.header("Panel de Control")

busqueda_texto = st.sidebar.text_input("Buscar en dataset (Categoría o Ciudad):", "")
categorias_disponibles = ['Todas'] + list(df['Categoria'].unique())
filtro_categoria = st.sidebar.selectbox("Filtrar por Categoría:", categorias_disponibles)


filtro_satisfaccion = st.sidebar.radio("Satisfacción mínima requerida:", [1, 2, 3, 4, 5], index=2)


min_venta, max_venta = int(df['Ventas'].min()), int(df['Ventas'].max())
filtro_ventas = st.sidebar.slider("Rango de Ventas:", min_venta, max_venta, (min_venta, max_venta))


df_filtrado = df.copy()

if filtro_categoria != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Categoria'] == filtro_categoria]

df_filtrado = df_filtrado[df_filtrado['Satisfaccion'] >= filtro_satisfaccion]
df_filtrado = df_filtrado[(df_filtrado['Ventas'] >= filtro_ventas[0]) & (df_filtrado['Ventas'] <= filtro_ventas[1])]

if busqueda_texto:
    df_filtrado = df_filtrado[
        df_filtrado['Categoria'].str.contains(busqueda_texto, case=False, na=False) |
        df_filtrado['Ciudad_Origen'].str.contains(busqueda_texto, case=False, na=False)
    ]

st.title("Dashboard Analítico en Producción")
st.markdown("---")

if st.sidebar.checkbox("Visualizar dataset completo / filtrado", value=False):
    st.subheader("Vista previa del Dataset")
    st.dataframe(df_filtrado, use_container_width=True)

st.subheader("Gráficas de Análisis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("*Gráfica 1: Ventas por Categoría (Barras)*")
    if not df_filtrado.empty:
        df_barras = df_filtrado.groupby('Categoria')['Ventas'].sum()
        st.bar_chart(df_barras)
    else:
        st.info("No hay datos para mostrar con los filtros actualizados.")

with col2:
    st.markdown("*Gráfica 2: Relación Ventas vs Satisfacción (Dispersión)*")
    if not df_filtrado.empty:
        st.scatter_chart(df_filtrado, x='Ventas', y='Satisfaccion', color='Categoria')
    else:
        st.info("No hay datos para mostrar.")

st.markdown("*Gráfica 3: Ventas por Ciudad de Origen (Líneas)*")
if not df_filtrado.empty:
    df_lineas = df_filtrado.groupby('Ciudad_Origen')['Ventas'].sum()
    st.line_chart(df_lineas)
else:
    st.info("No hay datos para mostrar.")

st.markdown("---")
st.header("Acerca de...")

autor_nombre = "Emiliano Rico Borbonio"
autor_matrícula = "sZ26004582"
ciudad_natal = "Orizaba, Veracruz"

st.markdown(f"""
* *Autor:* {autor_nombre}[span_0](start_span)[span_0](end_span)
* *Matrícula:* {autor_matrícula}[span_1](start_span)[span_1](end_span)
* *Ciudad Natal:* {ciudad_natal}[span_2](start_span)[span_2](end_span)
""")

map_data = pd.DataFrame({
    'lat': [18.8497],
    'lon': [-97.1036]
})
st.subheader(f"Mapa GPS de Ciudad Natal: {ciudad_natal}")
st.map(map_data, zoom=11)