from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .router import post, user, auth, vote
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional, List
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)        
app.include_router(user.router) 
app.include_router(auth.router) 
app.include_router(vote.router) 

@app.get("/")
def root():
    return {"Let's start our journey in making a API"}
