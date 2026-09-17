import streamlit as st
import sys
from pathlib import Path

# Add project root and src/ to sys.path so 'agent.*' imports resolve on Streamlit Cloud
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Existing imports continue below:
from agent.core import ExecutiveProductivityAgent
from agent.core import ExecutiveProductivityAgent
from agent.config import config

st.set_page_config(page_title="Executive Productivity Agent", page_icon="👔", layout="wide")

st.sidebar.title("Agent Controls")
st.sidebar.markdown(f"**Executive:** Arjun Malhotra (VP Sales)")
st.sidebar.markdown(f"**Model:** `{config.MISTRAL_MODEL}`")

simulated_now = st.sidebar.text_input(
    "Simulated Context Time",
    value=config.SIMULATED_NOW,
    help="Time-travel across the week (e.g., 2026-09-22T09:00:00 vs 2026-09-24T17:00:00)"
)

agent = ExecutiveProductivityAgent(simulated_now=simulated_now)

st.title("👔 Executive Productivity Agent")
st.caption("Personal Chief of Staff reasoning over emails, calendars, transcripts & voice notes.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar briefing button
if st.sidebar.button("Generate Today's Briefing", type="primary"):
    with st.spinner("Compiling executive briefing..."):
        resp = agent.generate_briefing(as_of=simulated_now)
        st.session_state.messages.append({
            "role": "user",
            "content": f"Give me my briefing as of {simulated_now}"
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": resp.answer,
            "citations": resp.citations,
            "trace": resp.reasoning_trace
        })

# Render conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander("🔍 Verified Sources & Reasoning Trace"):
                st.markdown("**Citations:**")
                for c in msg["citations"]:
                    st.write(f"- {c}")
                if msg.get("trace"):
                    st.markdown("**Tools Executed:**")
                    for t in msg["trace"]:
                        st.code(t, language="text")

# Chat input
if prompt := st.chat_input("Ask about your schedule, deliverables, or open risks..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing communications & calendars..."):
            resp = agent.answer_question(prompt)
            st.markdown(resp.answer)
            if resp.citations:
                with st.expander("🔍 Verified Sources & Reasoning Trace"):
                    st.markdown("**Citations:**")
                    for c in resp.citations:
                        st.write(f"- {c}")
                    if resp.reasoning_trace:
                        st.markdown("**Tools Executed:**")
                        for t in resp.reasoning_trace:
                            st.code(t, language="text")

    st.session_state.messages.append({
        "role": "assistant",
        "content": resp.answer,
        "citations": resp.citations,
        "trace": resp.reasoning_trace
    })