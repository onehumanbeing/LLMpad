import anthropic
from openai import OpenAI
import streamlit as st

anthropic_api_key = st.secrets["anthropic_api_key"]
openai_api_key = st.secrets["openai_api_key"]
anthropic_base_url = st.secrets["anthropic_base_url"] if "anthropic_base_url" in st.secrets else 'https://gba-api.thefans.life/claude'
gpt_base_url = st.secrets["gpt_base_url"] if "gpt_base_url" in st.secrets else 'https://gba-api.thefans.life/gpt/v1'
st.title("💬 Chatbot with GPT4 & Claude")

uploaded_file = st.file_uploader("Upload an file", type=("txt", "md"))

if "messages" not in st.session_state:
    st.session_state["messages"] = list()

if uploaded_file and not anthropic_api_key:
    st.info("Please add your Anthropic API key to continue.")

if uploaded_file:
    filedata = uploaded_file.read().decode()
    st.session_state["messages"] = [{"role": "user", "content": filedata}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(key="claude", placeholder="Your message with Claude"):
    if not anthropic_api_key:
        st.info("Please add your Anthropic API key to continue.")
        st.stop()
    # if len(st.session_state["claude_messages"]) == 0:
    #     st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    client = anthropic.Anthropic(api_key=anthropic_api_key, base_url=anthropic_base_url)
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=st.session_state.messages
    )
    msg = response.content[0].text
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

if prompt := st.chat_input(key="gpt4", placeholder="Your message with GPT4"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key, base_url=gpt_base_url)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4-0125-preview", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)