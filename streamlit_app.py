'''import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="📚 RAG Chatbot", layout="wide")
st.title("📚 RAG Chatbot (FastAPI + Qdrant + Ollama)")

# === File Upload ===
st.sidebar.header("📁 Upload Document")
file = st.sidebar.file_uploader("Upload .pdf, .docx, or .txt", type=["pdf", "docx", "txt"])

if file and st.sidebar.button("Upload"):
    files = {"file": (file.name, file.read())}
    response = requests.post(f"{API_BASE}/upload", files=files)
    if response.ok:
        result = response.json()
        st.sidebar.success(f"✅ Uploaded: {result['filename']}")
        st.session_state["last_collection"] = result["collection"]
    else:
        st.sidebar.error("Upload failed")

# === Ask a Question ===
st.subheader("💬 Ask a Question")
question = st.text_input("Enter your question")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            payload = {"question": question}
            res = requests.post(f"{API_BASE}/ask", json=payload)
            if res.ok:
                answer = res.json()
                st.success(answer["response"])

                if "fallback_answer" in answer:
                    st.info(f"LLM Fallback: {answer['fallback_answer']}")

                if "collection" in answer:
                    st.caption(f"Answered from: {answer['collection']}")
            else:
                st.error("Failed to get response.")'''
