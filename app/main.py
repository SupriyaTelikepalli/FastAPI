from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
while True:
    try:
        conn = psycopg2.connect(host='localhost',dbname='fastapidb', user='postgres',password='supriya',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection is successful')
        break
    except Exception as error:
        print('connecting to database failed')
        print("Error: ",error)
        time.sleep(2)



my_posts = [{"title":"Places in Texas","content":"Austin,Texas,Houston","id":1},{"title":"Food I like","content":"Pizza,Pasta,Soda","id":2}]
'''
def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p



def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
 
'''

@app.get("/")
def read_root():
    return {"message": "Welcome to API"}

@app.get("/sqlalchemy")
def test_post(db:Session = Depends(get_db)):
    return {"Status":"Success"}

@app.get("/posts")
def get_posts():
    cursor.execute("""select * from fastapi""")
    posts = cursor.fetchall()
    return{"data":posts}

'''
@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return{"new_post":f"title: {payload['title']} content: {payload['content']}"}
'''

#title: str, content: str using pydantic for validation
'''
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randint(1,1000000)
    my_posts.append(post_dict)
    return{"data":post_dict}


@app.get("/posts/{id}")
def get_post(id: int,response: Response):
    post = find_post(id)
    if not post:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'message': f"post with id: {id} was not found"}
    return{"post_details": post}  
'''

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO fastapi(title,content,published) VALUES(%s,%s,%s) returning * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data":new_post}

@app.get("/posts/{id}")
def get_post(id: int,response: Response):
    cursor.execute("""SELECT * FROM fastapi WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return{"post_details": post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,response: Response):
   cursor.execute("""DELETE FROM fastapi WHERE id = %s returning *""",((str(id))))
   deleted_index = cursor.fetchone()
   conn.commit()
   if deleted_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Requested id:{id} not found to delete")
   return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE fastapi SET title=%s,content=%s,published=%s where id=%s returning *""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Requested id:{id} doesn't exist")
    return {'message': updated_post}