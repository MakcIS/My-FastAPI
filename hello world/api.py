from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()

@app.get('/')
async def welcome()-> dict:
    return {"message": "Hello World"}

@app.get('/hello/{firstname}/{lastname}')
async def welcome_user(firstname:str, lastname:str)->dict:
    return {"message": f"Hello {firstname} {lastname}"}

@app.get('/order/{order_id}')
async def order(order_id:int)-> dict:
    return {"order": order_id}


@app.get("/user/{username}")
async def login(username: Annotated[str, Path(min_length=3, max_length=15, description='Enter your username')], 
                first_name: Annotated[str | None, Query(max_length=10, pattern='^J|s$')] = None):
    return {"user": username, "Name": first_name}

@app.get("/employee/{name}/company/{company}")
async def get_employee(name:str, company:str, department:str):
    return {"Employee": name, "Company": company, "Department": department}

@app.get('/user')
async def search(people: Annotated[list[str], Query()]):
    return {"users": people}

