from fastapi import FastAPI
import routes.login as LoginRoute
import routes.user as UserRoute
import routes.moderation as ModerationRoute
import routes.tutorial as TutorialRoute
import routes.article as ArticleRoute
import routes.challenges as ChallengeRoute
import routes.faq as FaqRoute
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import graypy
import os

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

logger = logging.getLogger("graylog_logger")
logger.setLevel(logging.INFO)

handler = graypy.GELFUDPHandler(os.getenv("GRAYLOG_HOST"), 12201)
logger.addHandler(handler)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://51.77.194.105:3000",
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
app.include_router(FaqRoute.router)
app.include_router(ChallengeRoute.router)

if __name__ == '__main__':
    uvicorn.run(app, reload=True)
