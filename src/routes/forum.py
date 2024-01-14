from typing import Optional
from fastapi import APIRouter, Depends, Request
from models.input.SubmitTutorialModel import SubmitTutorialModel
from models.input.ForumPostModel import ForumPostModel
from models.input.ForumCommentModel import ForumCommentModel
from models.response.CategoryResponseListModel import CategoryResponseListModel
from models.response.CompleteTutorialResponseModel import CompleteTutorialResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.ScoreboardTutorialIDListModel import ScoreboardTutorialIDListModel
from models.response.TutorialResponseListModel import TutorialResponseListModel, TutorialResponseListModelV2
from models.response.TutorialResponseModel import TutorialResponseModel, TutorialResponseModelV2
from models.response.ScoreboardTutorialMeListModel import ScoreboardTutorialMeListModel
from models.response.SuccessByIDModel import SuccessByIDModel
from models.response.SuccessMeModel import SuccessMeModel
from models.response.ForumPostResponseModel import ForumPostResponseModel
from models.response.ForumPostResponseListModel import ForumPostResponseListModel
from models.response.ForumCommentResponseModel import ForumCommentResponseModel
from database.Database import Database
from database.UserTutorialScore import UserTutorialScore
from database.CompletedTutorials import CompletedTutorials
from services.forum import ForumService
from services.tutorial import TutorialService
from starlette.responses import JSONResponse, Response
from services.utils.JWT import JWT
from services.utils.JWTChecker import JWTChecker
import requests, os, json
from services.utils.Log import Log
from services.utils.AdminChecker import AdminChecker


from services.utils.JWTChecker import JWTChecker

router = APIRouter(prefix='/forum')

get_all_posts_response = {
    200: {'model': ForumPostResponseListModel}
}

get_post_response = {
    200: {'model': ForumPostResponseModel}
}

@router.get('/all', tags=['forum'], responses=get_all_posts_response)
async def get_all_posts(r: Request) -> JSONResponse:
    """
    Récupérer tous les posts
    """
    Log.route_log(r, "posts routes", "open_route")
    post_list = ForumService.get_all_posts()
    return JSONResponse({'data': post_list}, status_code=200)

@router.get('/post/{post_id}/comments', tags=['forum'])
async def get_all_comments_post(r: Request, post_id: int) -> JSONResponse:
    """
    Récupérer tout les comments d'un post
    """
    Log.route_log(r, "tutorial routes", "open_route")
    comments = ForumService.get_all_comments_post(post_id)
    return JSONResponse({'data': comments}, status_code=200)

@router.post('/create', tags=['forum'], responses=get_post_response)
async def create_article(r: Request, forumPost: ForumPostModel, jwt = Depends(JWTChecker())) -> JSONResponse:
    """
    Création d'un article
    """
    Log.route_log(r, "article routes", "open_route")

    _jwt = JWT.decodeJWT(jwt)

    success = ForumService.create_post(forumPost.title, _jwt["uuid"], forumPost.description, 0, forumPost.category, "")
    if success:
        return JSONResponse({'success': 'Article created !'}, status_code=201)
    else:
        return JSONResponse({'error': "Can't create article"}, status_code=400)
    
@router.post('/comment/create', tags=['forum'], responses=get_post_response)
async def create_comment(r: Request, forumComment: ForumCommentModel, jwt = Depends(JWTChecker())) -> JSONResponse:
    """
    Création d'un article
    """
    Log.route_log(r, "forum routes", "open_route")

    _jwt = JWT.decodeJWT(jwt)

    success = ForumService.create_comment(forumComment.post_id, _jwt["uuid"], forumComment.text)
    if success:
        return JSONResponse({'success': 'Comment created !'}, status_code=201)
    else:
        return JSONResponse({'error': "Can't create Comment"}, status_code=400)


