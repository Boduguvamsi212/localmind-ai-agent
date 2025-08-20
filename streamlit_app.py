import streamlit as st
import requests
import os

BACKEND = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="LocalMind", page_icon="🧠")
st.title("🧠 LocalMind: AI That Thinks Without Internet")

with st.sidebar:
    st.header("Controls")
    use_tools = st.checkbox("Enable local tools (time, calc, notes)", True)
    if st.button("Clear History"):
        try:
            requests.delete(f"{BACKEND}/history", timeout=5)
            st.success("History cleared")
        except Exception as e:
            st.error(str(e))

prompt = st.text_area("Ask something (try: `time`, `calc 2+2*5`, `note buy milk`):", height=120)

col1, col2 = st.columns(2)
with col1:
    if st.button("Ask"):
        if prompt.strip():
            with st.status("Thinking…", expanded=False):
                try:
                    resp = requests.post(f"{BACKEND}/ask", json={"prompt": prompt, "use_tools": use_tools}, timeout=60)
                    data = resp.json()
                    st.session_state["last_answer"] = data.get("answer", "")
                except Exception as e:
                    st.session_state["last_answer"] = f"Error: {e}"
        else:
            st.warning("Type something first.")

with col2:
    if st.button("Refresh History"):
        pass

st.subheader("Answer")
st.write(st.session_state.get("last_answer", ""))

st.subheader("Recent History")
try:
    resp = requests.get(f"{BACKEND}/history?limit=20", timeout=5)
    for item in reversed(resp.json()):
        st.markdown(f"**{item['role']}**: {item['content']}  \n<small>{item['ts']}</small>", unsafe_allow_html=True)
except Exception as e:
    st.info("Start the FastAPI backend first.")
