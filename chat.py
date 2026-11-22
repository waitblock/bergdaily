import os

import streamlit as st
from dotenv import load_dotenv
from groq import APIError, Groq

load_dotenv()

st.set_page_config(page_title="Berg Daily Chat")
st.title("Berg Daily Chat")

api_key = os.getenv("GROQ_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask a question")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                completion = Groq(api_key=api_key).chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        *st.session_state.messages,
                    ],
                )
                answer = completion.choices[0].message.content or "No response returned."
            except APIError as exc:
                st.error(f"Groq request failed: {exc}")
            else:
                st.write(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
