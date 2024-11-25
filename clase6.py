#clase 6
#import random as rm #Renombrar/Abreviacion
#numeros = rm.sample(range(0,100),25)
#rint(numeros)
#from random import randint, choice

#colores = ["Rojo","verde","Azul","Amarillo","Negro","Purpura","Naranja"]
#color = choice(colores)
#print(f'El color elegido es el: {color}')

import streamlit as st
from groq import Groq


st.set_page_config(page_title="Argentina en decadencia", page_icon="🐼")
# Título de la aplicación
st.title("Bienvenido tonotos")

nombre = st.text_input("¡Cual es tu nombre?")
if st.button("Saludar"):
   st.write(f"¡Hola, {nombre}! gracias por venir a Talento Tech")

# MODELOS = ['modelo1', 'modelo2', 'modelo3'] 
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']


def actualizar_historial(rol, contenido, avatar):
        st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
        for mensaje in st.session_state.mensajes:
                with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
                        st.markdown(mensaje["content"])

def configurar_pagina():
 
# Agregamos un título principal a nuestra página
 st.title("Mi chat de IA")
 st.sidebar.title("Configuración de la IA") # Creamos un sidebar con un título.
 elegirModelo =  st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
 return elegirModelo



# mensaje = st.chat_input("Escribí tu mensaje:")

def crear_usuario_groq():
   clave_secreta = st.secrets["CLAVE_API"]
   return Groq (api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
     model=modelo,
     messages=[{"role": "user", "content": mensajeDeEntrada}],
     stream=True
)

def inicializar_estado():
    if "mensajes" not in st.session_state:
     st.session_state.mensajes = []


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
# Generamos un container que va a guardar el historial del chat
    contenedorDelChat = st.container(height=400,border=True)
# Abrimos el contenedor del chat y mostramos el historial.
    with contenedorDelChat:
        mostrar_historial()

# Creo una funciÃ³n main donde voy a ir agrupando todas las funciones de mi cÃ³digo para que corra
# todo desde una misma funciÃ³n
# "rellena la cadena de caracteres"
def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    
    mensaje = st.chat_input("Escriba tu mensaje: ")
    
    area_chat()
    
    if mensaje:
        actualizar_historial("user", mensaje, "🧑‍💻")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa,"🤖")
        st.rerun()

#Explicar que es esto, por que es importante que solo se ejecute si el archivo es el principal en streamlit.
if __name__ == "__main__":
    main()
