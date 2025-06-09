from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.agent1 import agent1
from agents.agent2 import agent2
from agents.agent3 import agent3
from agents.agent_classifier import classify_agent
from memory.episodic_memory import PostgresMemory  # <-- FIXED
import logging
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
memory = PostgresMemory() 
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a thread pool for running Ollama operations
thread_pool = ThreadPoolExecutor(max_workers=3)

class Query(BaseModel):
    message: str

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"status": "Server is running", "message": "Backend server is operational"}

@app.get("/health")
async def health_check():
    try:
        # Just check if agent1 works, don't log to memory
        test_message = "test"
        try:
            response = agent1(test_message)
            return {"status": "healthy", "message": "Server is operational"}
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(query: Query):
    try:
        message = query.message
        session_id = "default"  # Or your session logic

        # Save user message ONCE here
        if message.strip().lower() != "test":
            memory.save_message(session_id, "user", message)

        agent_id = classify_agent(message)
        if agent_id == 1:
            response = await asyncio.get_event_loop().run_in_executor(
                thread_pool, agent1, message, session_id
            )
        elif agent_id == 2:
            response = await asyncio.get_event_loop().run_in_executor(
                thread_pool, agent2, message, session_id
            )
        else:
            response = await asyncio.get_event_loop().run_in_executor(
                thread_pool, agent3, message, session_id
            )

        # Save agent response ONCE here
        if message.strip().lower() != "test":
            memory.save_message(session_id, "agent", response)

        return {"response": response, "agent_used": agent_id}
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
