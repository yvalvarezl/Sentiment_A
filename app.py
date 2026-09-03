import json
from textblob import TextBlob, Word
import pandas as pd
import streamlit as st
from googletrans import Translator
from streamlit_lottie import st_lottie

# Cargar la animación
with open('Jumping Emoji.json') as source:
    animation = json.load(source)

# Layout superior
col1, col2 = st.columns([1, 3])

with col1:
    st_lottie(animation, width=140, key="emoji_anim")

with col2:
    st.title('🎈 Emocionómetro Infantil')
    st.subheader("Acompaña el bienestar emocional de tus hijos a través de sus escritos 💛")

st.write("Escribe o pega aquí el cuento, nota o entrada del diario que escribió tu hijo para descubrir cómo se siente.")

translator = Translator()

# --- SIDEBAR INTERACTIVO Y PERSONALIZABLE ---
with st.sidebar:
    st.header("⚙️ Personaliza la experiencia")
    nombre_nino = st.text_input("👤 Nombre de tu hijo/a:", value="tu hijo/a")
    edad = st.slider("🎂 Edad aproximada:", min_value=3, max_value=15, value=8)

# --- BLOQUE DE ANÁLISIS ---
with st.expander('🔍 Analizar texto', expanded=True):
    text = st.text_area(f'Escribe el texto de {nombre_nino} aquí:', height=120)
    boton_enviar = st.button('🚀 Enviar / Analizar escrito')
    
    if boton_enviar:
        if text.strip() == "":
            st.warning("Por favor, ingresa un texto antes de enviar.")
        else:
            # 1. Traducción y análisis con TextBlob
            translation = translator.translate(text, src="es", dest="en")
            trans_text = translation.text
            blob = TextBlob(trans_text)
            polarity = blob.sentiment.polarity
            
            # 2. Análisis por presencia de palabras/raíces
            text_lower = text.lower()
            
            palabras_feliz = ["feliz", "felicidad", "alegre", "content", "emocionad", "gust", "encant", "genial", "super", "sonre", "happy", "joy", "glad"]
            palabras_triste = ["triste", "depri", "llor", "solo", "solit", "aburr", "feo", "dolor", "pena", "no me deja", "no me quiere", "no puedo", "enoj", "rabia", "molest", "sad", "cry"]

            es_feliz = any(p in text_lower for p in palabras_feliz)
            es_triste = any(p in text_lower for p in palabras_triste)
            
            if es_feliz and not es_triste:
                polarity = max(polarity, 0.5)
            elif es_triste and not es_feliz:
                polarity = min(polarity, -0.5)

            st.markdown("---")
            st.markdown(f"### 📊 Resultado para **{nombre_nino}**")
            
            # 3. Resultado directo (sin barrita)
            if polarity > 0.15:
                st.success(f"😄 **{nombre_nino} está feliz.**")
            elif polarity < -0.15:
                st.error(f"😔 **{nombre_nino} está triste.**")
            else:
                st.info(f"😐 **{nombre_nino} está normal.**")
