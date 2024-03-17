from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default is set to true
    rating: Optional[int] = None

my_post = [{"title":"title of post 1", "content":"content of post 1", "id":1}, 
           {"title":"title of post 2", "content":"content of post 2", "id":2}]

def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

app = FastAPI()

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def get_posts(post: Post):
    print("Post added") #converts to dictionary
    post_dict = post.model_dump()
    post_dict['id'] = randrange(1,100000)
    my_post.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/")
def get_posts():
    return {"data": my_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message': f"post with id: {id} was not found"}
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {'data': post_dict}