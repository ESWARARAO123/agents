from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.agent1 import agent1
from agents.agent2 import agent2
from agents.agent3 import agent3
from agents.agent_classifier import classify_agent
from memory.episodic_memory import memory
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
        # Test only agent1 with a simple message
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
        logger.info(f"Received chat request with message: {query.message}")
        
        message = query.message

        # Store to memory
        memory.save_message(message)

        # Determine which agent to use
        agent_id = classify_agent(message)
        logger.info(f"Selected agent: {agent_id}")

        # Process with appropriate agent using thread pool
        try:
            if agent_id == 1:
                response = await asyncio.get_event_loop().run_in_executor(
                    thread_pool, agent1, message
                )
            elif agent_id == 2:
                response = await asyncio.get_event_loop().run_in_executor(
                    thread_pool, agent2, message
                )
            else:
                response = await asyncio.get_event_loop().run_in_executor(
                    thread_pool, agent3, message
                )

            logger.info(f"Generated response: {response}")
            memory.save_response(response)
            return {"response": response, "agent_used": agent_id}
        except Exception as agent_error:
            logger.error(f"Agent {agent_id} error: {str(agent_error)}")
            logger.error(traceback.format_exc())
            if "timeout" in str(agent_error).lower():
                raise HTTPException(
                    status_code=504,
                    detail="The AI model took too long to respond. Please try again in a few moments."
                )
            raise HTTPException(
                status_code=500,
                detail=f"Error in agent {agent_id}: {str(agent_error)}"
            )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
