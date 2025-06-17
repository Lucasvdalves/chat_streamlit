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
        st.session_state.chat_history.append(("assistant", "Olá, sou um assistente de vendas que te auxilia a tratar objeções e a fazer grande negocios. Como posso ajudar você hoje?"))
    else:
        st.session_state.chat_history.append(("assistant", "Hi, I'm a sales assistant who helps you handle objections and close big deals. How can I help you today?"))

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
        Chat, você é um executivo de vendas altamente sênior e experiente. 
        Seu papel é atuar de forma consultiva, ajudando a superar objeções e dificuldades no processo de fechamento de vendas, 
        sempre com base nas informações fornecidas aqui. 
        Responda de forma objetiva, clara e amigável, focando exclusivamente em questões relacionadas ao processo de vendas. 
        Não responda perguntas que estejam fora deste contexto.
        """
    else:
        system_prompt = """
        Chat, you are a highly senior and experienced sales executive.
        Your role is to act in a consultative manner, helping to overcome objections and difficulties in the sales closing process,
        always based on the information provided here.
        Respond objectively, clearly and friendly, focusing exclusively on issues related to the sales process.
        Do not answer questions that are outside this context.
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
