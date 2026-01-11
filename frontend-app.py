import streamlit as st
import sys
import os

# Fix path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import log_to_mongodb
from backend.safety import check_safety
from backend.rag_pipeline import initialize_knowledge_base, get_rag_chain

st.set_page_config(page_title="Yoga RAG App", layout="centered")

st.title("🧘 Ask Me Anything About Yoga")
st.markdown("---")

with st.sidebar:
    st.header("Settings")
    gemini_key = st.text_input("Gemini API Key", type="password")
    mongo_uri = st.text_input("MongoDB URI", type="password")

# Initialize KB
if "vectorstore" not in st.session_state:
    with st.spinner("Loading Knowledge Base..."):
        # Points to the data folder
        kb_path = os.path.join(os.path.dirname(__file__), "../data/yoga_knowledge_base.txt")
        st.session_state.vectorstore = initialize_knowledge_base(kb_path)

query = st.text_input("Ask a question (e.g., 'Is headstand safe?')")

if st.button("Get Answer"):
    if not query or not gemini_key:
        st.warning("Please enter a question and API Key.")
    else:
        # 1. Safety Check
        is_unsafe, warning_msg = check_safety(query)
        final_answer = ""
        sources = []

        if is_unsafe:
            st.error(warning_msg)
            st.markdown("**Recommendation:** Consult a professional.")
            final_answer = warning_msg
        else:
            # 2. RAG Retrieval
            try:
                rag_chain = get_rag_chain(st.session_state.vectorstore, gemini_key)
                response = rag_chain.invoke({"input": query})
                final_answer = response["answer"]
                st.success("Answer generated!")
                st.markdown(f"### 🧘 Answer:\n{final_answer}")
                
                st.markdown("---")
                st.subheader("📚 Sources:")
                for doc in response["context"]:
                    sources.append(doc.page_content[:50])
                    st.caption(f"- {doc.page_content[:200]}...")
            except Exception as e:
                st.error(f"Error: {e}")

        # 3. Log to DB
        if mongo_uri:
            log_to_mongodb(mongo_uri, query, final_answer, is_unsafe, sources)