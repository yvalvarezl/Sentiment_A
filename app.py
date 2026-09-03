# --- AJUSTE DE SENSIBILIDAD PARA NIÑOS ---
text_lower = text.lower()

# 1. Detección de Frustración / Tristeza
palabras_tristes_frustracion = [
    "no me deja", "no me quiere llevar", "no me quiere", "no puedo", 
    "triste", "enojado", "molesto", "aburrido", "llorar", "feo", "solo"
]

# 2. Detección directa de Felicidad / Entusiasmo
palabras_felices = [
    "feliz", "contento", "contenta", "alegre", "emocionado", 
    "emocionada", "me gusta", "me encanta", "genial", "super"
]

# Regla para Tristeza / Frustración
if any(p in text_lower for p in palabras_tristes_frustracion) and polarity >= 0.0:
    polarity = -0.35

# Regla para Felicidad directa (Si contiene palabras felices y dio neutral o muy bajo)
elif any(p in text_lower for p in palabras_felices) and polarity <= 0.2:
    polarity = 0.6  # Asigna un valor claramente positivo
