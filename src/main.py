from fastapi import FastAPI, Depends
import routes.login as LoginRoute
import routes.user as UserRoute
import routes.moderation as ModerationRoute
import routes.tutorial as TutorialRoute
import routes.article as ArticleRoute
from services.utils.JWTChecker import JWTChecker
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

description = open('../docs/swaggerDescription.md', 'r', encoding='utf-8').read()
tags_metadata = [
    {
        'name': 'user',
        'description': 'User interaction with the website'
    },
    {
        'name': 'tutorial',
        'description': 'Tutorial user interaction only'
    },
    {
        'name': 'article',
        'description': 'Article routes for the blog'
    },
    {
        'name': 'moderation',
        'description': 'Moderation route for moderators and administrators'
    },
    {
        'name': 'admin',
        'description': 'Admin management only'
    }
]

app = FastAPI(
    title="Block2School",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata,
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(LoginRoute.router)
app.include_router(UserRoute.router)
app.include_router(ModerationRoute.router)
app.include_router(TutorialRoute.router)
app.include_router(ArticleRoute.router)

# @app.get("/", dependencies=[Depends(JWTChecker())], tags=['root'])
# def read_root():
#     return {"hello": 'world'}

if __name__ == '__main__':
    uvicorn.run(app, reload=True)