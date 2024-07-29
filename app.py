from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import json
from agent import Agent
from dotenv import load_dotenv
import uuid

load_dotenv()

app = FastAPI(title="Search Smart API")

# Initialize the agent
agent = Agent(system_prompt=open("system_prompt.txt", 'r').read())

# Dictionary to store conversation histories
conversations = {}

class MessageRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class MessageResponse(BaseModel):
    response: str
    sources: Optional[list] = None
    thread_id: str

@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    thread_id = request.thread_id

    if not thread_id:
        # Create a new thread if not provided
        thread_id = str(uuid.uuid4())
        conversations[thread_id] = []

    if thread_id not in conversations:
        raise HTTPException(status_code=404, detail="Thread not found")

    # Append user message to conversation history
    conversations[thread_id].append({"role": "user", "text": request.message})

    # Get response from agent
    response, sources = agent.send_message(request.message)

    # Append assistant response to conversation history
    conversations[thread_id].append({"role": "assistant", "text": response})

    # Save conversation history to file
    save_conversation(thread_id, conversations[thread_id])

    return MessageResponse(response=response, sources=sources, thread_id=thread_id)

def save_conversation(thread_id: str, history: list):
    os.makedirs("./conversations", exist_ok=True)
    with open(f"./conversations/{thread_id}.json", "w") as f:
        json.dump(history, f)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)