from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents.agent1 import agent1
from agents.agent2 import agent2
from agents.agent3 import agent3
from memory.episodic_memory import memory

app = FastAPI()

class Query(BaseModel):
    message: str
    agent_id: int  # 1, 2, or 3

@app.post("/chat")
async def chat(query: Query):
    message = query.message
    agent_id = query.agent_id

    # Store to memory
    memory.save_message(message)

    if agent_id == 1:
        response = agent1(message)
    elif agent_id == 2:
        response = agent2(message)
    else:
        response = agent3(message)

    memory.save_response(response)
    return {"response": response}
