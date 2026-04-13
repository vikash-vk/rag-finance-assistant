import streamlit as st
from process_incoming import answer_query

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Personal Finance Assistant",
    page_icon="💰",
    layout="centered"
)

# =========================
# HEADER
# =========================
st.markdown("""
# 💰 AI Personal Finance Assistant

Learn personal finance concepts from the  
**Zerodha Varsity - Personal Finance for Beginners** playlist.

Ask questions and get guidance on what to watch and where.
""")

# =========================
# PLAYLIST LINK
# =========================
st.info(
    "📺 This assistant is based on the Zerodha Varsity playlist. "
    "[Watch the full playlist here](https://youtube.com/playlist?list=PLX2SHiKfualHj_3Ms2t8cCd9tUpQHA9MW&si=gBp61ZcqpARH-ySS)"
)

# =========================
# INPUT SECTION
# =========================
st.markdown("### 🔍 Ask a Question")

query = st.text_input(
    "",
    placeholder="e.g. What is an emergency fund?"
)

# =========================
# PROCESS
# =========================
if query:
    with st.spinner("Thinking..."):

        response, results = answer_query(query)

    # =========================
    # ERROR HANDLING
    # =========================
    if results is None:
        st.error(response)
        st.stop()

    # =========================
    # OUTPUT
    # =========================
    with st.container():
        st.markdown("#### 🧠 Answer")
        st.write(response)
# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown("""
<div style='text-align: center; font-size: 14px;'>

⚡ Built using Retrieval-Augmented Generation (RAG)  
🤖 Powered by local LLM (Ollama)  
📚 Based on Zerodha Varsity

</div>
""", unsafe_allow_html=True)