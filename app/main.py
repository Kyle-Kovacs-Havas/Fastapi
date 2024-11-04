from fastapi import FastAPI
from . import models, config
from .database import engine
from .routers import users, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware
#venv\Scripts\activate
#uvicorn app.main:app --reload

print(config.settings.database_name)

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://google.com"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
    return {"Hello": "Hi there, this is the change"}

