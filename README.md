# 🧠 TechWriter.AI — Agentic AI for Intelligent Documentation

> **An AI-powered documentation assistant that reads codebases, SQL, and notebooks — then automatically generates technical documentation, release notes, and Q&A answers.**

---

## 🚀 Overview

**TechWriter.AI** combines **Agentic AI**, **NLP**, and **RAG** to act as a *technical writing co-pilot*.  
It can:
- Ingest Python, SQL, Markdown, or notebook files  
- Understand structure and dependencies  
- Generate clear technical documentation in multiple styles (developer guide, user manual, blog post)  
- Review drafts for accuracy, completeness, and clarity  
- Support interactive Q&A over the project’s content  

---

## 🏗️ System Architecture

![Architecture Diagram](./docs/techwriter_ai_architecture.png)

**Core layers:**
1. **Ingestion & Indexing** – Converts `.py`, `.sql`, `.ipynb`, `.md`, `.docx` to text, extracts metadata, and stores embeddings in a vector database (Chroma/FAISS).  
2. **RAG Context Retrieval** – Fetches top-k context chunks relevant to each query or documentation request.  
3. **Agentic Orchestration** – Multi-agent workflow built with LangGraph or CrewAI:
   - 🧩 *Code Analyst Agent* → extracts logic, IO, dependencies  
   - ✍️ *Technical Writer Agent* → drafts documentation  
   - ✅ *Reviewer Agent* → checks style, factuality, and structure  
4. **LLM Inference** – Uses OpenAI / Llama / Mistral for reasoning, summarization, and writing.  
5. **UI & Exports** – Streamlit or Gradio app for uploads, queries, and exports to Markdown/PDF/Confluence.  
6. **Observability** – LangSmith or custom logging for tracing, evaluation, and quality control.

---

## 📂 Repository Structure

```bash
TechWriter-AI/
├─ app/
│  └─ ui.py                   # Streamlit / Gradio interface
├─ core/
│  ├─ ingestion.py             # File loading and conversion
│  ├─ indexing.py              # Embeddings + vector store
│  ├─ retriever.py             # RAG pipeline
│  ├─ prompts/
│  │  ├─ system_writer.md
│  │  ├─ system_analyst.md
│  │  ├─ system_reviewer.md
│  │  └─ styles/
│  │     ├─ developer_doc.md
│  │     ├─ user_manual.md
│  │     └─ blog_post.md
│  └─ exporters.py             # Markdown / PDF / Confluence exports
├─ agents/
│  ├─ graph_orchestrator.py
│  ├─ code_analyst.py
│  ├─ tech_writer.py
│  └─ reviewer.py
├─ tools/
│  ├─ ast_utils.py
│  ├─ sql_parser.py
│  └─ git_utils.py
├─ data/
│  ├─ index/
│  └─ samples/
├─ tests/
│  └─ test_end_to_end.py
├─ docs/
│  └─ techwriter_ai_architecture.pdf
├─ requirements.txt
└─ README.md
