import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

# 🔐 Cargar credenciales desde secrets.toml
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="prueba-movies-419b2")

def load_data(db):
    docs = db.collection('movies').stream()
    data = [doc.to_dict() for doc in docs]
    return pd.DataFrame(data)

# Inicio de la app
st.title("🎬 Catálogo de Filmes")
data = load_data(db)

# Sidebar principal
st.sidebar.title("🎛 Opciones")
st.sidebar.markdown("Usa las siguientes herramientas para explorar y agregar filmes.")

# Diagnóstico inicial
if data.empty:
    st.warning("⚠️ No hay filmes en la base de datos.")
else:
    st.write("📊 Datos cargados:")
    st.dataframe(data.head())

# Justo después de cargar los datos
st.write("Datos cargados:")
st.write(data)

if st.sidebar.checkbox("Mostrar todos los filmes"):
    st.subheader("Lista completa de filmes")
    st.dataframe(data)

titulo = st.sidebar.text_input("Buscar por título")
if st.sidebar.button("Buscar título"):
    resultados = data[data['name'].str.lower().str.contains(titulo.lower())]
    st.subheader(f"Filmes que contienen: {titulo}")
    st.dataframe(resultados)

directores = data['director'].dropna().unique()
opcion = st.sidebar.selectbox("Selecciona un director", directores)

if st.sidebar.button("Buscar por director"):
    filtrados = data[data['director'] == opcion]
    st.subheader(f"Filmes dirigidos por: {opcion}")
    st.write(f"Total: {filtrados.shape[0]}")
    st.dataframe(filtrados)

st.sidebar.markdown("---")
st.sidebar.subheader("🎬 Agregar nuevo filme")
titulo_nuevo = st.sidebar.text_input("Título")
compania_nuevo = st.sidebar.text_input("Compañia")
director_nuevo = st.sidebar.text_input("Director")
genero = st.sidebar.text_input("Género")

if st.sidebar.button("Agregar filme"):
    nuevo = {
        "name": titulo_nuevo,
        "company": compania_nuevo,
        "director": director_nuevo,
        "genre": genero
    }
    db.collection("movies").add(nuevo)
    st.sidebar.success("Filme agregado exitosamente")
