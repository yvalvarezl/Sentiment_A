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

# --- BLOQUE DE ANÁLISIS ---
with st.expander('🔍 Analizar texto', expanded=True):
    text = st.text_area(f'Escribe el texto de {nombre_nino} aquí:', height=120)
    
    # Botón para activar el análisis al hacer clic
    boton_enviar = st.button('🚀 Enviar / Analizar escrito')
    
    if boton_enviar:
        if text.strip() == "":
            st.warning("Por favor, ingresa un texto antes de enviar.")
        else:
            translation = translator.translate(text, src="es", dest="en")
            trans_text = translation.text
            blob = TextBlob(trans_text)
            
            polarity = round(blob.sentiment.polarity, 2)
            
            # --- AJUSTE DE SENSIBILIDAD PARA NIÑOS (Detección de Frustración / Tristeza) ---
            text_lower = text.lower()
            palabras_tristes_frustracion = [
                "no me deja", "no me quiere llevar", "no me quiere", "no puedo", 
                "triste", "enojado", "molesto", "aburrido", "llorar", "feo", "solo"
            ]
            
            # Si el texto contiene frases de deseo no cumplido o tristeza implícita y la polaridad dio neutral (0.0):
            if any(p in text_lower for p in palabras_tristes_frustracion) and polarity >= 0.0:
                polarity = -0.35  # Asignamos un sesgo negativo razonable
            
            # Mapeo de polaridad a porcentaje (0% a 100%)
            porcentaje_animo = int((polarity + 1) * 50)
            
            st.markdown("---")
            st.markdown(f"### 📊 Resultado para **{nombre_nino}** ({edad} años)")
            
            # Barrita visual de emoción
            st.markdown("#### 🌡️ **Emocionómetro Visual**")
            col_emo1, col_emo2, col_emo3 = st.columns([1, 6, 1])
            with col_emo1:
                st.write("😔 *(Triste)*")
            with col_emo2:
                st.progress(porcentaje_animo)
            with col_emo3:
                st.write("😄 *(Feliz)*")
            
            # Interpretación adaptada según la emoción
            if polarity > 0.1:
                st.success(f"😄 **{nombre_nino} expresa un sentimiento Positivo ({porcentaje_animo}%)**")
                st.write(f"💡 **Consejo:** Aprovecha este momento para preguntarle qué fue lo que más le gustó de su día y reforzar sus emociones positivas.")
            elif polarity < -0.1:
                st.error(f"😔 **{nombre_nino} expresa un sentimiento de Tristeza, Incomodidad o Frustración ({porcentaje_animo}%)**")
                st.write(f"💡 **Consejo:** Acércate con empatía a {nombre_nino}. Escúchalo/a sin interrumpir y valida sus emociones diciéndole que es normal sentirse así cuando no podemos hacer algo que deseamos.")
            else:
                st.info(f"😐 **{nombre_nino} expresa un sentimiento Neutral o Calmo ({porcentaje_animo}%)**")
                st.write(f"💡 **Consejo:** El texto narra situaciones sin reflejar emociones intensas. Puedes preguntarle libremente cómo se sintió durante lo que relata.")
