from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from services.article import ArticleService
from models.input.ArticleModel import ArticleModel
from models.input.IdModel import IdModel
from models.response.ArticleResponseModel import ArticleResponseModel
from models.response.ArticleListResponseModel import ArticleListResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.SuccessResponseModel import SuccessResponseModel
from services.utils.AdminChecker import AdminChecker

get_all_articles_response = {
    200: {'model': ArticleListResponseModel}
}

get_article_response = {
    200: {'model': ArticleResponseModel}
}

update_article_response = {
    200: {'model': ArticleResponseModel},
    400: {'model': ErrorResponseModel}
}

create_article_response = {
    201: {'model': SuccessResponseModel},
    400: {'model': ErrorResponseModel}
}

delete_article_response = {
    200: {'model': SuccessResponseModel},
    400: {'model': ErrorResponseModel}
}

router = APIRouter(prefix='/article')

@router.get('/all', tags=['article'], responses=get_all_articles_response)
async def get_all_articles():
    articles = ArticleService.get_all_articles()
    return JSONResponse({'data': articles})

@router.get('/id/{id}', tags=['article'], responses=get_article_response)
async def get_article(id: int):
    article = ArticleService.get_article(id)
    return JSONResponse(article)

@router.post('/create', tags=['article'], dependencies=[Depends(AdminChecker(1))], responses=create_article_response)
async def create_article(article: ArticleModel):
    success = ArticleService.create_article(article.title, article.markdownUrl, article.author, article.shortDescription)
    if success:
        return JSONResponse({'success': 'Article created !'}, status_code=201)
    else:
        return JSONResponse({'error': "Can't create article"})

@router.patch('/update', tags=['article'], dependencies=[Depends(AdminChecker(1))], responses=update_article_response)
async def update_article(article: ArticleModel):
    if article.id == -1:
        return JSONResponse({'error': 'Invalid ID'}, status_code=400)
    else:
        result = ArticleService.update_article(article.id, article.title, article.markdownUrl, article.shortDescription)
        if result:
            return JSONResponse(article)
        else:
            return JSONResponse({'error': "Can't update article"}, status_code=400)

@router.delete('/delete', tags=['article'], dependencies=[Depends(AdminChecker(1))], responses=delete_article_response)
async def delete_article(id: IdModel):
    if id.id != None:
        result = ArticleService.delete_article(id)
        if result:
            return JSONResponse({'success': 'Article deleted !'})
        else:
            return JSONResponse({'error': 'An error occured while deleting article'}, status_code=400)
    else:
        return JSONResponse({'error': 'Unknown article ID'}, status_code=400)