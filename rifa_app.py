import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io

# Inicializar estado si no existe
if 'numeros_disponibles' not in st.session_state:
    st.session_state.numeros_disponibles = list(range(1, 101))
if 'numero_elegido' not in st.session_state:
    st.session_state.numero_elegido = None

st.title("Rifa Colaboración")
st.subheader("Muchas gracias por colaborar! Sortea 20/07, $300")

st.markdown("### Números disponibles:")

# Crear tabla 10x10 con los números disponibles
tabla = []
for i in range(10):
    fila = []
    for j in range(10):
        numero = i * 10 + j + 1
        if numero in st.session_state.numeros_disponibles:
            fila.append(str(numero))
        else:
            fila.append("❌")
    tabla.append(fila)

df_tabla = pd.DataFrame(tabla)
st.dataframe(df_tabla, use_container_width=True)

# Entrada de número
numero_ingresado = st.number_input("Elegí tu número del 1 al 100:", min_value=1, max_value=100, step=1)
if st.button("Aceptar"):
    if numero_ingresado in st.session_state.numeros_disponibles:
        st.session_state.numeros_disponibles.remove(numero_ingresado)
        st.session_state.numero_elegido = numero_ingresado
        st.success(f"Tu número {numero_ingresado} fue reservado exitosamente")
    else:
        st.error("Ese número ya no está disponible. Probá con otro.")

# Generar imagen de confirmación
if st.session_state.numero_elegido:
    img = Image.new('RGB', (400, 250), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_body = ImageFont.truetype("arial.ttf", 20)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    d.text((10, 20), "Rifa Colaboración", fill=(0, 0, 0), font=font_title)
    d.text((10, 80), f"Tu número: {st.session_state.numero_elegido}", fill=(0, 0, 0), font=font_body)
    d.text((10, 120), "Sortea: 20/07", fill=(0, 0, 0), font=font_body)
    d.text((10, 160), "$300", fill=(0, 0, 0), font=font_body)
    d.text((10, 200), "Gracias por colaborar!", fill=(0, 0, 0), font=font_body)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.image(img)
    st.download_button("Descargar comprobante", data=buf.getvalue(), file_name=f"rifa_numero_{st.session_state.numero_elegido}.png", mime="image/png")
