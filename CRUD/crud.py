from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory='templates')

class Message(BaseModel):
    id: int | None = None
    text: str
    model_config = {
        "json_schema_extra": {
            "examples":
            [
                {
                    "text": "Simple message"
                }
            ]
        }
    }

messages_db = []

@app.get('/')
async def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, 'message.html', {'messages': messages_db})

@app.get(path='/message/{message_id}')
async def get_message(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse(request, 'message.html', {'message': messages_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Message not found')

@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message:Message) -> str:
    if messages_db:
        message.id = max(messages_db, key=lambda x: x.id).id + 1
    else:
        message.id = 0
    messages_db.append(message)
    return 'Message created!'

@app.put("/message/{message_id}") 
async def update_message(message_id:int, message:str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return "Message updated!"
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Message not found')

@app.delete("/message/{message_id}")
async def delete_message(message_id:int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Message not found')
        
@app.delete("/")
async def kill_message_all()->str:
    messages_db.clear()
    return "All messages deleted!"