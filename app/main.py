from fastapi import FastAPI, status, HTTPException, Response, Depends 
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, users, auth, vote
from .database import engine
from . import models

app = FastAPI()

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "root directory..."}
# models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)