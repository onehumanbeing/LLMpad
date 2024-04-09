import anthropic
from openai import OpenAI
import streamlit as st

anthropic_api_key = st.secrets["anthropic_api_key"]
openai_api_key = st.secrets["openai_api_key"]
anthropic_base_url = st.secrets["anthropic_base_url"] if "anthropic_base_url" in st.secrets else 'https://gba-api.thefans.life/claude'
gpt_base_url = st.secrets["gpt_base_url"] if "gpt_base_url" in st.secrets else 'https://gba-api.thefans.life/gpt/v1'
st.title("📝 File Q&A with Claude3")

uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not anthropic_api_key:
    st.info("Please add your Anthropic API key to continue.")

if uploaded_file and question and anthropic_api_key:
    article = uploaded_file.read().decode()
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n
    {article}\n\n\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=anthropic_api_key, base_url=anthropic_base_url)
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-3-opus-20240229",
        # max_tokens=4096,
        max_tokens_to_sample=4096
    )
    st.write("### Answer")
    st.write(response.completion)

# OPENAI
st.title("💬 Chatbot with GPT4")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
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