import streamlit as st
import google.generativeai as genai
from functions import get_secret, reset_chat

api_key = get_secret("API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Adiciona campo para selecionar o idioma
language = st.sidebar.selectbox("Escolha o idioma / Choose the language:", ["Português", "English"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.chat_history:
    if language == "Português":
        st.session_state.chat_history.append(("assistant", "Olá, sou um assistente de vendas. Como posso ajudar você hoje?"))
    else:
        st.session_state.chat_history.append(("assistant", "Hello, I am a sales assistant. How can I help you today?"))

if st.sidebar.button("Reset chat"):
    reset_chat()

for role, message in st.session_state.chat_history:
    st.chat_message(role).write(message)

user_message = st.chat_input("Digite sua mensagem..." if language == "Português" else "Type your message...")

if user_message:
    st.chat_message("user").write(user_message)
    st.session_state.chat_history.append(("user", user_message))
    
    if language == "Português":
        system_prompt = """
        Chat, você é um executivo de vendas altamente sênior, 
        e seu papel é ser consultivo e ajudar a lidar com 
        objeções de vendas com base nos dados que recebe aqui. 
        Você não deve responder a nenhuma outra pergunta fora de contexto, 
        seja objetivo e amigável com suas respostas.
        """
    else:
        system_prompt = """
        Chat, you are a highly senior sales executive,  
        and your role is to be consultative and help deal with 
        sales objections based on the data you receive here. 
        You should not answer any other questions that are out of context, 
        be objective and friendly with your answers.
        """

    full_input = f"{system_prompt}\n\nUser message:\n\"\"\"{user_message}\"\"\""
    
    context = [
        *[
            {"role": role, "parts": [{"text": msg}]} for role, msg in st.session_state.chat_history
        ],
        {"role": "user", "parts": [{"text": full_input}]}
    ]

    response = model.generate_content(
        full_input,
        generation_config={
            "max_output_tokens": 1000
        }
    )

    assistant_reply = response.text

    st.chat_message("assistant").write(assistant_reply)
    st.session_state.chat_history.append(("assistant", assistant_reply))
