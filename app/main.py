from fastapi import FastAPI
from blog import  models
from blog.database import engine
from blog.routers import blog, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.routers)
app.include_router(blog.routers)
app.include_router(user.routers)
