from codecs import raw_unicode_escape_decode
import email
from turtle import title
from typing import List 
from unittest.mock import NonCallableMock
from click import password_option
from fastapi import FastAPI, Depends , status, Response , HTTPException
from . import schemas, models
from .database import SessionLocal, engine 
from sqlalchemy.orm import Session 


import blog

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)

def create(request : schemas.Blog , db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog' , response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.put("/blog/update/{id}")
def updateBlog(id, request:schemas.Blog, db:Session=Depends(get_db)):
   blog= db.query(models.Blog).filter(models.Blog.id == id).first()
   
   if not blog:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with id {id} not found')
   else:
    db.query(models.Blog).filter(models.Blog.id == id).update(request.dict())

    db.commit()
    db.refresh(blog)

    return blog

@app.get("/blog/{id}", status_code=200 )
def show(id, response: Response, db:Session=Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} not available")
    

    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.post('/user')
def create_user(request : schemas.User , db: Session = Depends(get_db)):
    new_user = models.User(name= request.name, email=request.email, password = request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user