import streamlit as st
from typing import List, Any
from backend.core import run_llm


def format_sources(context_docs: List[Any]) -> List[str]:
    """Extract unique source URLs from context documents."""
    sources = []
    for doc in (context_docs or []):
        meta = getattr(doc, "metadata", None) or {}
        source = meta.get("source")
        if source and source not in sources:
            sources.append(source)
    return sources


st.set_page_config(
    page_title="LangChain Documentation Helper",
    page_icon="📚",
    layout="centered"
)

st.title("📚 LangChain Documentation Helper")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.subheader("About")
    st.write("Ask questions about LangChain documentation and get AI-powered answers with sources.")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📄 Sources"):
                for source in message["sources"]:
                    st.write(f"- {source}")

# Chat input
if prompt := st.chat_input("Ask a question about LangChain..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching documentation..."):
            result = run_llm(query=prompt)
            answer = result["answer"]
            sources = format_sources(result.get("context", []))

        st.markdown(answer)

        if sources:
            with st.expander("📄 Sources"):
                for source in sources:
                    st.write(f"- {source}")

    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
