# AI Agent Chat System

This project is a multi-agent AI chat system with a web frontend and a FastAPI backend. It can classify user messages and route them to the appropriate agent: General Assistant, SQL Query Generator, or Calculator. The backend uses Ollama for LLM inference and supports basic conversation memory.

---

## Features

- **Multi-agent:** General, SQL, and Calculator agents.
- **Automatic classification:** Messages are routed to the correct agent.
- **Memory:** Stores conversation history (see `backend/memory/episodic_memory.py`).
- **Modern UI:** React + Material UI frontend, desktop-friendly.
- **Backend:** FastAPI, LangChain, Ollama.

---

## Prerequisites

- **Python 3.9+**
- **Node.js 16+** (for frontend)
- **Ollama** running locally (see [Ollama docs](https://ollama.com/))
- **Ollama models:** `mistral` (and optionally `llama3`, `codestral`)

---

## Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start Ollama** and pull required models:
   ```bash
   ollama serve
   ollama pull mistral
   # Optionally:
   # ollama pull llama3
   # ollama pull codestral
   ```

3. **Run the FastAPI backend:**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8001
   ```

---

## Frontend Setup

1. **Install Node dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the frontend dev server:**
   ```bash
   npm run dev
   ```
   The app will be available at [http://localhost:3001](http://localhost:3001).

---

## Usage

- Open [http://localhost:3001](http://localhost:3001) in your browser.
- Type a message and send. The system will classify and route your message to the correct agent.
- Example prompts:
  - "Show all users from customers where age > 25" (SQL)
  - "Calculate 5 + 3" (Calculator)
  - "Tell me a joke" (General)

---

## Notes

- **Ollama** must be running locally with the required models.
- The backend expects requests from `http://localhost:3001` (see CORS settings).
- Conversation memory is basic and stored in memory (see `backend/memory/episodic_memory.py`).

---

## Project Structure

```
backend/
  app.py
  agents/
    agent1.py
    agent2.py
    agent3.py
    agent_classifier.py
  memory/
    episodic_memory.py
frontend/
  src/
    App.jsx
    main.jsx
  index.html
  package.json
```

---

## Troubleshooting

- **Ollama not running:** Make sure `ollama serve` is active and models are pulled.
- **CORS errors:** Ensure backend and frontend are running on the correct ports.
- **Model errors:** If you see model errors, check that the model names in the code match those pulled in Ollama.

---

## License

MIT License