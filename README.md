# 🤖 AI Multi-Agent Assistant

An intelligent Multi-Agent AI Assistant built using **LangGraph**, **LangChain**, **Groq LLM**, and **Streamlit**.

Instead of relying on a single LLM for every query, this application intelligently classifies user requests and routes them to specialized AI agents for more accurate and efficient responses.

---

## 🚀 Features

- 🧠 Intelligent Query Classification using LLM
- 💻 Dedicated Coding Agent
- 🌤 Weather Agent using Tool Calling
- 🌍 Google Search Agent using You.com Search
- 🔀 Dynamic Routing with LangGraph
- 💬 Interactive Streamlit Chat Interface
- 🧾 Persistent Conversation Memory
- ⚡ Powered by Groq LLM
- 🛠 Modular Agent Architecture
- 📈 Easily Extendable with New Agents

---

# 🏗 Architecture

```
                    User Question
                          │
                          ▼
               Question Classification
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
   Coding Agent     Weather Agent   Search Agent
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                   Final Response
```

---

# ⚙ Tech Stack

- Python
- LangGraph
- LangChain
- Groq LLM
- Streamlit
- Pydantic
- You.com Search Tool
- Tool Calling

---

# 📂 Project Structure

```
AI-Multi-Agent-Assistant/

│── app.py
│── graph.py
│── requirements.txt
│── README.md
│── .env.example
```

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Multi-Agent-Assistant.git
```

Move into the project

```bash
cd AI-Multi-Agent-Assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key
YDC_API_KEY=your_you_api_key
```

Run the Streamlit application

```bash
streamlit run app.py
```

---

# 🧠 Workflow

1. User submits a question.
2. LangGraph sends the question to the Classification Node.
3. The classifier identifies the category.
4. The workflow routes the query to the appropriate agent.
5. The selected agent generates the response.
6. The answer is displayed in the Streamlit interface.

---

# 💻 Supported Agents

## 💻 Coding Agent

Handles:

- DSA
- Algorithms
- Debugging
- Python
- C++
- Java
- Coding Interview Questions

---

## 🌤 Weather Agent

Provides weather information using LangChain Tool Calling.

---

## 🌍 Google Search Agent

Retrieves information using the You.com Search Tool.

---

# 📸 Demo

Streamlit -- [https://ai-multi-agent.streamlit.app/]
---

# 📌 Future Improvements

- Streaming Responses
- Multi-turn Agent Memory
- Real Weather API Integration
- Research Agent
- PDF RAG Agent
- SQL Database Agent
- Image Generation Agent
- Voice Assistant
- Authentication
- Docker Deployment

---

# 🎯 Learning Outcomes

This project demonstrates:

- Multi-Agent Systems
- Agentic AI
- LangGraph Workflows
- Conditional Routing
- Tool Calling
- LLM Structured Output
- Prompt Engineering
- State Management
- Streamlit Deployment

---

# 🤝 Contributing

Contributions are welcome.

Feel free to fork this repository and submit pull requests.

---

# 📄 License

MIT License

---

# 👨‍💻 Author

**Veer Tiwari**

AI Engineer | Machine Learning | Generative AI

If you found this project useful, consider giving it a ⭐.
