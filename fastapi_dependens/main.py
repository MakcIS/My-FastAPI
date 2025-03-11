from fastapi import FastAPI, Depends, Query, HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

log_user = []

def log_client(request: Request):
    log_user.append(request.headers)

app = FastAPI(dependencies=[Depends(log_client)])

class Paginator:
    def __init__(self, limit: int = 10, page:int = 1):
        self.limit = limit
        self.page = page

    def __call__(self, limit:int):
        if limit < self.limit:
            return [{'limit': self.limit, 'page': self.page}]
        else:
            return [{'limit': limit, 'page': self.page}]

class Post(BaseModel):
    id: int
    text: str

db = []

async def get_post_or_404(id:int):
    try:
        return db[id]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get('/message/{id}')
async def get_message(post: Post = Depends(get_post_or_404)) -> dict:
    return post

@app.post('/message', status_code=status.HTTP_201_CREATED)
async def create_message(post:Post):
    post.id = len(db)
    db.append(post)
    return f'Message created!'

@app.put('/message/{id}')
async def update_message(post:Post = Depends(get_post_or_404)):
    pass

@app.delete('/message/{id}')
async def delete_message(post:Post = Depends(get_post_or_404)):
    pass

my_pagination = Paginator()

@app.get('/users')
async def all_users(pagination: list = Depends(my_pagination)):
    return {'users': pagination}


async def sub_dependency(request:Request) -> str:
    return request.method

async def main_dependency(sub_dependency_value: str = Depends(sub_dependency)) -> str:
    return sub_dependency_value

@app.get('/test/')
async def test_endpoin(test:str = Depends(main_dependency)):
    return test

async def pagination_path_func(page:int):
    if page < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Page does not exist')
    if page == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid page value')
    
async def pagination_func(limit:int = Query(10, ge=0), page:int=1):
    return {'limit': limit, 'page': page}

@app.get('/messages', dependencies=[Depends(pagination_path_func)])
async def all_messages(pagination: dict = Depends(pagination_func)):
    return {'messages': pagination}


@app.get('/log_user')
async def print_log_user():
    return {'user': log_user}