from fastapi import FastAPI

app = FastAPI()

messages_db = {0: "First post in FastAPI"}

@app.get('/')
async def get_all_messages() -> dict:
    return messages_db

@app.get('/message/{message_id}')
async def get_message(message_id:int) -> str:
    return messages_db[message_id]

@app.post("/message")
async def create_message(message:str) -> str:
    pass

@app.put("/message/{message_id}") 
async def update_message(message_id:int, message:str) -> str:
    pass

@app.delete("/message/{message_id}")
async def delete_message(message_id:int) -> str:
    pass

@app.delete("/")
async def kill_message_all()->str:
    pass