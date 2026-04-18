import streamlit as st
import plotly.graph_objects as go
from dispatcher import Dispatcher

st.set_page_config(page_title="The White Box", layout="wide")

if "dispatcher" not in st.session_state:
    p_a = {"name": "Zero", "style": "冷徹"}
    p_b = {"name": "Eve", "style": "情緒的"}
    st.session_state.dispatcher = Dispatcher("models/Bonsai-8B-v1.gguf", p_a, p_b)
    st.session_state.history = []
    st.session_state.running = False

with st.sidebar:
    st.title("Control")
    if st.button("Start/Pause"): st.session_state.running = not st.session_state.running
    st.session_state.dispatcher.watcher_state = st.radio("Watcher", ["Active", "Asleep"])

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Emotions")
    emo_a = st.session_state.dispatcher.emotions["AgentA"].get_state()
    emo_b = st.session_state.dispatcher.emotions["AgentB"].get_state()
    fig = go.Figure()
    categories = ['congruence', 'resonance', 'friction', 'attenuation']
    fig.add_trace(go.Scatterpolar(r=[emo_a[c] for c in categories], theta=categories, fill='toself', name='A'))
    fig.add_trace(go.Scatterpolar(r=[emo_b[c] for c in categories], theta=categories, fill='toself', name='B'))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Log")
    for h in st.session_state.history:
        with st.chat_message(h["role"].lower()): st.write(f"{h['role']}: {h['content']}")

if st.session_state.running:
    turn = st.session_state.dispatcher.step()
    if turn:
        st.session_state.history.append(turn)
        st.rerun()
