from fastapi import FastAPI,Response,status,HTTPException, Depends,APIRouter
from typing import Optional,List
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user),limit:Optional[int]=10,skip:Optional[int]=0,search:Optional[str]=""):
    # cursor.execute("""select * from fastapi""")
    # posts = cursor.fetchall()
    print(search)
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

'''
@router.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return{"new_post":f"title: {payload['title']} content: {payload['content']}"}


#title: str, content: str using pydantic for validation

@router.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randint(1,1000000)
    my_posts.routerend(post_dict)
    return{"data":post_dict}


@router.get("/posts/{id}")
def get_post(id: int,response: Response):
    post = find_post(id)
    if not post:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'message': f"post with id: {id} was not found"}
    return{"post_details": post}  
'''

@router.post("/",response_model=schemas.Post,status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate,db:Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO fastapi(title,content,published) VALUES(%s,%s,%s) returning * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,response: Response,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    # cursor.execute("""SELECT * FROM fastapi WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    return post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,response: Response,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    deleted_post_query = db.query(models.Post).filter(models.Post.id==id)
    # cursor.execute("""DELETE FROM fastapi WHERE id = %s returning *""",((str(id))))
    # deleted_index = cursor.fetchone()
    # conn.commit()
    deleted_post = deleted_post_query.first()
    if deleted_post.first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Requested id:{id} not found to delete")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE fastapi SET title=%s,content=%s,published=%s where id=%s returning *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id==id)
    my_post = updated_post.first()
    if my_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Requested id:{id} doesn't exist")
    if my_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    updated_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return updated_post.first()