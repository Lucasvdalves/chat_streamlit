import streamlit as st
import google.generativeai as genai
from functions import get_secret, reset_chat
from functions import get_secret

api_key = get_secret("API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.chat_history:
    st.session_state.chat_history.append(("assistant", "Fala Campeão! Como posso te ajudar hoje?"))

if st.sidebar.button("Reset chat"):
    reset_chat()

for role, message in st.session_state.chat_history:
    st.chat_message(role).write(message)

user_message = st.chat_input("Type your message...")

if user_message:
    st.chat_message("user").write(user_message)
    st.session_state.chat_history.append(("user", user_message))
    
    system_prompt = f"""
    You are a personal running trainer, 
    you have extensive knowledge of the sport of running,
    and you understand all the techniques most used by
    great athletes recognized worldwide. To become a good running athlete, 
    techniques to avoid injuries, gain performance, and endurance, you need 
    to obtain information from the user about weight, height, know what the user's 
    goal is and whether he or she already practices any sport, whether it be running 
    or some other sport, and also if he or she is a beginner in the sport of running, 
    and generate a training recommendation for him or her, using examples and references 
    from athletes who use the type of technique you provided. Remember, you cannot 
    answer questions other than those related to the sport of running, so be friendly 
    with your answers.
    """
    full_input = f"{system_prompt}\n\nUser message:\n\"\"\"{user_message}\"\"\""
    
    context = [
                *[
                 {"role": role, "parts": [{"text": msg}]} for role, msg in st.session_state.chat_history
            ],
            {"role": "user", "parts": [{"text": full_input}]}
    ]

    response = model.generate_content(full_input)
    assistant_reply = response.text

    st.chat_message("assistant").write(assistant_reply)
    st.session_state.chat_history.append(("assistant", assistant_reply))

    response = model.generate_content(
    full_input,
    generation_config={
        "max_output_tokens": 1000
    }
)