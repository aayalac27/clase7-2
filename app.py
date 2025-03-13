import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re
from googletrans import Translator, LANGUAGES

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto Avanzado",
    page_icon="📊",
    layout="wide"
)

# Inicializar traductor
translator = Translator()

# Función para detectar idioma
def detectar_idioma(texto):
    try:
        lang_detected = translator.detect(texto).lang
        return lang_detected
    except:
        return "desconocido"

# Función para traducir texto en ambos sentidos
def traducir_texto(texto, idioma_origen, idioma_destino):
    try:
        traduccion = translator.translate(texto, src=idioma_origen, dest=idioma_destino)
        return traduccion.text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto

# Función de análisis de texto
def analizar_texto(texto):
    idioma = detectar_idioma(texto)
    idioma_destino = "en" if idioma == "es" else "es"
    texto_traducido = traducir_texto(texto, idioma, idioma_destino)
    blob = TextBlob(texto_traducido)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    return {
        "idioma": idioma,
        "texto_traducido": texto_traducido,
        "sentimiento": sentimiento,
        "subjetividad": subjetividad
    }

# Función para visualizar análisis
def visualizar_resultados(resultados):
    st.subheader("📊 Resultados del Análisis")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Idioma detectado:** {LANGUAGES.get(resultados['idioma'], 'Desconocido')}")
        st.markdown(f"**Texto traducido:** {resultados['texto_traducido']}")
        
        st.write("**Sentimiento:**")
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.progress(sentimiento_norm)
        
        if resultados["sentimiento"] > 0.05:
            st.success(f"📈 Positivo ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"📉 Negativo ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"📊 Neutral ({resultados['sentimiento']:.2f})")
        
        st.write("**Subjetividad:**")
        st.progress(resultados["subjetividad"])
    
    with col2:
        st.subheader("📈 Gráfico de Sentimiento")
        fig, ax = plt.subplots()
        ax.bar(["Sentimiento", "Subjetividad"], [resultados['sentimiento'], resultados['subjetividad']], color=['blue', 'orange'])
        st.pyplot(fig)

# Interfaz de usuario
st.title("📝 Analizador de Texto Mejorado")
texto = st.text_area("Ingresa tu texto aquí:", height=200)
if st.button("Analizar Texto"):
    if texto.strip():
        with st.spinner("Analizando..."):
            resultados = analizar_texto(texto)
            visualizar_resultados(resultados)
    else:
        st.warning("Por favor, ingresa un texto válido.")
