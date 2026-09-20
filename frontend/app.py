import streamlit as st
from api_client import check_backend_health, query_rag_assistant

st.set_page_config(
    page_title="DevOps RAG Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🛠️ DevOps & Infrastructure RAG Assistant")
st.caption("Grounded technical answers from Docker, Kubernetes, and Linux documentation.")

# Display backend connectivity status in sidebar
with st.sidebar:
    st.header("⚙️ System Status")
    is_healthy = check_backend_health()
    if is_healthy:
        st.success("Backend API: Online (Connected)")
    else:
        st.error("Backend API: Offline")
        st.warning("Ensure FastAPI server is running on http://localhost:8000")
        
    st.markdown("---")
    st.markdown("**Core Tech Stack:**")
    st.markdown("- **Model:** Llama 3.2 (via Ollama)")
    st.markdown("- **Vector Store:** ChromaDB")
    st.markdown("- **Embeddings:** all-MiniLM-L6-v2")
    st.markdown("- **Backend:** FastAPI")

# Initialize chat message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask me any technical question about Docker, Kubernetes, Git, or Linux configurations.", "sources": []}
    ]

# Render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("📚 Cited Documentation Sources"):
                for src in message["sources"]:
                    st.markdown(f"- `{src}`")

# Handle user query input
if prompt := st.chat_input("Ask a technical question (e.g., How do I list pods in Kubernetes?)..."):
    # Append and render user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Fetch response from backend with spinner
    with st.chat_message("assistant"):
        with st.spinner("Searching documentation and generating grounded response..."):
            result = query_rag_assistant(prompt)

        if "error" in result:
            st.error(result["error"])
        else:
            answer = result.get("answer", "")
            sources = result.get("sources", [])
            st.markdown(answer)
            if sources:
                with st.expander("📚 Cited Documentation Sources"):
                    for src in sources:
                        st.markdown(f"- `{src}`")
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })