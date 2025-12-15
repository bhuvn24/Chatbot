# 💰 Private GenAI Financial Advisor

A privacy-focused AI-powered financial chatbot built with **Streamlit**, **LangChain**, and **RAG (Retrieval-Augmented Generation)** architecture. Get personalized financial advice while keeping your data secure.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)

## ✨ Features

- 🤖 **Intelligent Query Routing** - Automatically routes queries to the appropriate domain-specific knowledge base
- 📚 **RAG Architecture** - Retrieves relevant documents from vector databases for accurate, context-aware responses
- 🔒 **Privacy-Focused** - Designed with data privacy in mind using local models
- 🌐 **Web Fallback** - Automatically searches the web when local knowledge is insufficient
- 💬 **Conversational Memory** - Maintains context across multiple exchanges
- 📊 **Data Visualization** - Displays financial charts and graphs in responses
- 👤 **Human-in-the-Loop** - Feedback system for continuous improvement

## 🏗️ Architecture

```
src/
├── app.py              # Main Streamlit application
├── config/             # Configuration files and constants
├── core/
│   ├── memory.py       # Conversation memory management
│   ├── rag_chain.py    # RAG chain implementation
│   └── router.py       # Query routing logic
├── models/
│   ├── llm.py          # Large Language Model integration
│   └── slm.py          # Small Language Model integration
└── utils/
    ├── conversation.py # Conversational response handling
    ├── embeddings.py   # Text embedding utilities
    ├── retrievers.py   # Vector database retrieval
    ├── visualizer.py   # Chart visualization
    └── web_search.py   # Web search fallback
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bhuvn24/Chatbot.git
   cd Chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   ```

5. **Run the application**
   ```bash
   streamlit run src/app.py
   ```

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web application framework |
| `langchain` | LLM orchestration framework |
| `langchain-groq` | Groq LLM integration |
| `langchain-ollama` | Local Ollama model support |
| `faiss-cpu` | Vector similarity search |
| `sentence-transformers` | Text embeddings |
| `firecrawl-py` | Web scraping |
| `beautifulsoup4` | HTML parsing |
| `matplotlib` | Data visualization |

## 🎯 Usage

1. Launch the application using `streamlit run src/app.py`
2. Select your preferred mode from the dropdown
3. Type your financial question in the chat input
4. Receive AI-powered responses with relevant context
5. Provide feedback to help improve responses

### Query Modes

- **Auto** - Automatically detects the best domain for your query
- **Hardcoded** - Manually select a specific financial domain
- **All DB** - Search across all knowledge bases

## 📁 Data

The `data/` directory contains vector databases for different financial domains. The `dataset/` directory stores the source documents used to build these knowledge bases.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**bhuvn24**

- GitHub: [@bhuvn24](https://github.com/bhuvn24)

---

⭐ Star this repo if you find it helpful!
