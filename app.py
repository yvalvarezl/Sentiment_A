import json
from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
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
    
    # 1. Datos del Niño/a
    nombre_nino = st.text_input("👤 Nombre de tu hijo/a:", value="tu hijo/a")
    edad = st.slider("🎂 Edad aproximada:", min_value=3, max_value=15, value=8)
    
    st.markdown("---")
    
    # 2. Selector de Intuición del Padre
    intuicion = st.selectbox(
        "🤔 ¿Cómo notas a " + nombre_nino + " hoy?",
        ["No lo sé aún", "Parece feliz/entusiasmado", "Parece tranquilo/normal", "Parece triste/molesto"]
    )
    
    st.markdown("---")
    
    # 3. Explicación interactiva con Tabs
    st.subheader("💡 Guía de Análisis")
    tab_pol, tab_sub = st.tabs(["Polaridad", "Subjetividad"])
    
    with tab_pol:
        st.caption(
            "Indica la carga emocional del escrito (-1 muy negativo a +1 muy positivo). "
            "Nos ayuda a detectar si hay tristeza, frustración o alegría implícita."
        )
    with tab_sub:
        st.caption(
            "Mide qué tanto expresa sus propias emociones (1.0) frente a solo contar hechos u objetos externos (0.0)."
        )

# --- BLOQUE DE ANÁLISIS ---
with st.expander('🔍 Analizar texto', expanded=True):
    text = st.text_area(f'Escribe el texto de {nombre_nino} aquí:', height=120)
    
    if text:
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)
        
        st.markdown("---")
        st.markdown(f"### 📊 Resultado para **{nombre_nino}** ({edad} años)")
        
        # Interpretación adaptada según la edad y resultados
        if polarity > 0.1:
            st.success(f"😊 **{nombre_nino} expresa un sentimiento Positivo**")
            st.write(f"💡 **Consejo:** Aprovecha este momento para preguntarle qué fue lo que más le gustó de su día y reforzar sus emociones positivas.")
        elif polarity < -0.1:
            st.error(f"😔 **{nombre_nino} expresa un sentimiento de Tristeza, Incomodidad o Molestia**")
            st.write(f"💡 **Consejo:** Acércate con empatía a {nombre_nino}. Escúchalo/a sin interrumpir y valida sus emociones diciéndole que es normal sentirse así.")
        else:
            st.info(f"😐 **{nombre_nino} expresa un sentimiento Neutral o Calmo**")
            st.write(f"💡 **Consejo:** El texto narra situaciones sin reflejar emociones intensas. Puedes preguntarle libremente cómo se sintió durante lo que relata.")

        # Detalle de Subjetividad
        st.markdown("---")
        st.markdown("#### 📝 Nivel de Expresión Emocional")
        if subjectivity > 0.5:
            st.write(f"✨ {nombre_nino} está expresando sus **sentimientos y opiniones de forma muy personal**.")
        else:
            st.write(f"📖 {nombre_nino} está haciendo una **descripción objetiva o contando un suceso**.")

        # Métricas técnicas
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Puntaje de Emoción (Polaridad)", polarity)
        col_m2.metric("Puntaje de Expresión (Subjetividad)", subjectivity)
