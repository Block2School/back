from fastapi import APIRouter, Depends, Request
from models.input.BanModel import BanModel
from models.input.CategoryModel import CategoryModel
from models.input.CategoryNameModel import CategoryNameModel
from models.input.ModModel import ModModel
from models.input.TutorialEditModel import TutorialEditModel
from models.input.TutorialModel import TutorialModel
from models.input.UnbanModel import UnbanModel
from models.input.CreateMarkdownModel import CreateMarkdownModel
from models.response.AvailableMarkdownResponseModel import AvailableMarkdownResponseModel
from models.response.BanResponseModel import BanResponseModel
from models.response.CreateMarkdownResponseModel import CreateMarkdownResponseModel
from models.response.ErrorResponseModel import ErrorResponseModel
from models.response.SuccessResponseModel import SuccessResponseModel
from models.response.ToggleTutorialResponseModel import ToggleTutorialResponseModel
from models.response.UnbanResponseModel import UnbanResponseModel
from models.response.BanListResponseModel import BanListResponseModel
from models.response.AccountResponseModelList import AccountResponseModelList
from models.response.IsAdminResponseModel import IsAdminResponseModel
from models.input.IdModel import IdModel
from services.article import ArticleService
from services.moderation import ModerationService
from services.tutorial import TutorialService
from starlette.responses import JSONResponse
from services.utils.AdminChecker import AdminChecker
from services.utils.JWT import JWT
from services.utils.JWTChecker import JWTChecker
from services.utils.Log import Log

router = APIRouter(prefix='/admin')

banlist_responses = {
    200: {'model': BanListResponseModel},
    400: {'model': ErrorResponseModel}
}
ban_responses = {
    200: {'model': BanResponseModel},
    400: {'model': ErrorResponseModel}
}
unban_responses = {
    200: {'model': UnbanResponseModel},
    400: {'model': ErrorResponseModel}
}
set_mod_responses = {
    200: {'model': ModModel},
    400: {'model': ErrorResponseModel}
}
create_tutorial_responses = {
    200: {'model': SuccessResponseModel},
    400: {'model': ErrorResponseModel}
}
update_tutorial_responses = {
    200: {'model': SuccessResponseModel},
    400: {'model': ErrorResponseModel}
}
toggle_tutorial_responses = {
    200: {'model': ToggleTutorialResponseModel},
    400: {'model': ErrorResponseModel}
}
create_category_responses = {
    200: {'model': SuccessResponseModel},
    400: {'model': ErrorResponseModel}
}
update_category_responses = {
    200: {'model': SuccessResponseModel},
    400: {'model': ErrorResponseModel}
}
delete_category_responses = {
    200: {'model': SuccessResponseModel},
    400: {'model': ErrorResponseModel}
}
create_markdown_responses = {
    201: {'model': CreateMarkdownResponseModel},
    400: {'model': ErrorResponseModel}
}
available_markdown_responses = {
    200: {'model': AvailableMarkdownResponseModel},
    400: {'model': ErrorResponseModel}
}

get_all_users_responses = {
    200: {'model': AccountResponseModelList}
}

is_admin_responses = {
    200: {'model': IsAdminResponseModel}
}

@router.get('/is_admin', tags=['admin'], dependencies=[Depends(JWTChecker())], responses=is_admin_responses)
async def is_admin(r: Request, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Vérifie qu'un utilisateur est bien administrateur sur l'application
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "moderation routes", jwt["uuid"])
    is_admin = ModerationService.is_admin(jwt['uuid'])
    return JSONResponse({'is_admin': is_admin}, status_code=200)

@router.get('/users', dependencies=[Depends(AdminChecker(2))], tags=['admin'], responses=get_all_users_responses)
async def get_all_users(r: Request, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Récupération de tous les utilisateurs de la plateforme
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    users = ModerationService.get_all_users()
    return JSONResponse({'data': users}, status_code=200)

@router.get('/banlist/{uuid}', dependencies=[Depends(AdminChecker(1))], tags=['moderation'], responses=banlist_responses)
async def get_banlist(r: Request, uuid: str, credentials: str = Depends(AdminChecker(1))) -> JSONResponse:
    """
    Récupération de la liste des bannissements d'un utilisateur
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    datas = ModerationService.get_banlist(uuid)
    return JSONResponse({"data": datas}, status_code=200)

@router.post('/ban', dependencies=[Depends(AdminChecker(1))], tags=['moderation'], responses=ban_responses)
async def ban(r: Request, ban_model: BanModel, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Bannir un utilisateur de la plateforme
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "moderation routes", jwt["uuid"])
    if ban_model.uuid == None:
        return JSONResponse({"error": "UUID not provided"}, status_code=400)
    else:
        is_banned = ModerationService.ban(ban_model.uuid, jwt['uuid'], ban_model.reason, ban_model.expires)
        if is_banned:
            return JSONResponse({"uuid": ban_model.uuid, "banned_by": jwt['uuid'], "reason": ban_model.reason, "expires": ban_model.expires}, status_code=200)
        else:
            return JSONResponse({"error": "Cannot ban this user"}, status_code=400)

@router.post('/unban', dependencies=[Depends(AdminChecker(1))], tags=['moderation'], responses=unban_responses)
async def unban(r: Request, revoke: UnbanModel, credentials: str = Depends(JWTChecker())) -> JSONResponse:
    """
    Débannir un utilisateur de la plateforme
    """
    jwt = JWT.decodeJWT(credentials)
    Log.route_log(r, "moderation routes", jwt["uuid"])
    if revoke.uuid == None:
        return JSONResponse({"error": "UUID not provided"}, status_code=400)
    else:
        is_unbanned = ModerationService.unban(revoke.uuid, jwt['uuid'], revoke.reason)
        if is_unbanned:
            return JSONResponse({"uuid": revoke.uuid, "revoked_by": jwt['uuid'], "reason": revoke.reason}, status_code=200)
        else:
            return JSONResponse({"error": "Cannot unban this user"}, status_code=400)

@router.post('/mod', dependencies=[Depends(AdminChecker(2))], tags=['admin'])
async def set_mod(r: Request, mod_model: ModModel, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Rendre un utilisateur modérateur sur la plateforme
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    if mod_model.uuid == None:
        return JSONResponse({"error": "UUID not provided"}, status_code=400)
    else:
        is_changed = ModerationService.set_mod(mod_model.uuid, mod_model.role)
        if is_changed:
            return JSONResponse({"uuid": mod_model.uuid, "role": mod_model.role}, status_code=200)
        else:
            return JSONResponse({"error": "Cannot change mod role of this user"}, status_code=400)

@router.post('/tuto/create', dependencies=[Depends(AdminChecker(2))], tags=['admin'], responses=create_tutorial_responses)
async def create_tutorial(r: Request, tutorial_model: TutorialModel, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Créer un tutoriel
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    if tutorial_model.answer == None:
        return JSONResponse({'error': 'Unknown answer'}, status_code=400)
    elif tutorial_model.category == None:
        return JSONResponse({'error': 'Unknown category'}, status_code=400)
    elif tutorial_model.markdownUrl == None:
        return JSONResponse({'error': 'Unknown markdown URL'}, status_code=400)
    elif tutorial_model.title == None:
        return JSONResponse({'error': 'Unknown title'}, status_code=400)
    elif tutorial_model.startCode == None:
        return JSONResponse({'error': 'Unknown start code'}, status_code=400)
    elif tutorial_model.shouldBeCheck == None:
        return JSONResponse({'error': 'Unknown should be check boolean'}, status_code=400)
    elif tutorial_model.input == None:
        return JSONResponse({"error": 'Unknown input'}, status_code=400)
    elif tutorial_model.points == None:
        return JSONResponse({"error": 'Unknown points'}, status_code=400)
    result = TutorialService.create_tutorial(tutorial_model.title, tutorial_model.markdownUrl, tutorial_model.startCode, tutorial_model.category, tutorial_model.answer, tutorial_model.shouldBeCheck, tutorial_model.input, tutorial_model.points, tutorial_model.default_language, tutorial_model.image, tutorial_model.short_description, tutorial_model.estimated_time)
    if result:
        return JSONResponse({"success": "Tutorial created !"}, status_code=200)
    else:
        return JSONResponse({"error": "This tutorial already exists"}, status_code=400)

@router.patch('/tuto/update', dependencies=[Depends(AdminChecker(2))], tags=['admin'], responses=update_tutorial_responses)
async def edit_tutorial(r: Request, tutorial_model: TutorialEditModel, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Editer un tutoriel
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    if tutorial_model.id == None:
        return JSONResponse({'error': 'Unknown id'}, status_code=400)
    elif tutorial_model.title == None:
        return JSONResponse({'error': 'Unknown title'}, status_code=400)
    elif tutorial_model.markdownUrl == None:
        return JSONResponse({'error': 'Unknown markdown URL'}, status_code=400)
    elif tutorial_model.category == None:
        return JSONResponse({'error': 'Unknown category'}, status_code=400)
    elif tutorial_model.answer == None:
        return JSONResponse({'error': 'Unknown answer'}, status_code=400)
    elif tutorial_model.startCode == None:
        return JSONResponse({'error': 'Unknown start code'}, status_code=400)
    elif tutorial_model.shouldBeCheck == None:
        return JSONResponse({'error': 'Unknown should be check'}, status_code=400)
    elif tutorial_model.input == None:
        return JSONResponse({"error": 'Unknown input'}, status_code=400)
    elif tutorial_model.points == None:
        return JSONResponse({"error": 'Unknown points'}, status_code=400)
    result = TutorialService.update_tutorial(tutorial_model.id, tutorial_model.title, tutorial_model.markdownUrl, tutorial_model.category, tutorial_model.answer, tutorial_model.startCode, tutorial_model.shouldBeCheck, tutorial_model.input, tutorial_model.points)
    if result:
        return JSONResponse({'success': 'Updated tutorial !'}, status_code=200)
    else:
        return JSONResponse({'error': 'Can\'t update tutorial'}, status_code=400)

@router.patch('/tuto/toggle', dependencies=[Depends(AdminChecker(2))], tags=['admin'], responses=toggle_tutorial_responses)
async def enable_disable_tutorial(r: Request, id_model: IdModel, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    @deprecated

    Activer ou désactiver un tutoriel
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    if id_model.id == None:
        return JSONResponse({'error': 'Tutorial ID not provided'}, status_code=400)
    tutorial = TutorialService.get_tutorial(id_model.id)
    enabled = tutorial.get('enabled')
    enabled = not enabled
    result = TutorialService.toggle_tutorial(id_model.id, enabled)
    if result:
        return JSONResponse(result, status_code=200)
    return JSONResponse({'error': 'Can\'t toggle this tutorial'}, status_code=400)

@router.post('/category/create', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=create_category_responses)
async def create_category(r: Request, category: CategoryModel, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Créer une catégorie de tutoriels
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = TutorialService.create_category(category.name, category.description, category.image)
    if result:
        return JSONResponse({'success': 'Created category ' + category.name}, status_code=200)
    return JSONResponse({'error': 'Could not create the category'}, status_code=400)

@router.patch('/category/update', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=update_category_responses)
async def update_category(r: Request, category: CategoryModel, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Modifier une catégorie de tutoriels
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = TutorialService.update_category(category.name, category.description, category.image)
    if result:
        return JSONResponse({'success': 'Updated category ' + category.name}, status_code=200)
    return JSONResponse({'error': 'Could not update the category'}, status_code=400)

@router.delete('/category/delete', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=delete_category_responses)
async def delete_category(r: Request, name: CategoryNameModel, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Supprimer une catégorie de tutoriels
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = TutorialService.delete_category(name.name)
    if result:
        return JSONResponse({'success': 'Category deleted'}, status_code=200)
    return JSONResponse({'error': 'Could not delete the category'}, status_code=400)

@router.post('/article/create_markdown', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=create_markdown_responses)
async def create_markdown(r: Request, markdown: CreateMarkdownModel, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Créer un markdown pour les articles
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = ArticleService.create_markdown(markdown.name, markdown.content)
    if result and result['success'] == True:
        return JSONResponse({'success': f'Markdown "{markdown.name}" created', 'markdown_url': result}, status_code=200)
    return JSONResponse({'error': 'Could not create the markdown'}, status_code=400)

@router.get('/article/available_markdown', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=available_markdown_responses)
async def get_available_markdown(r: Request, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Récupérer la liste des markdowns disponibles pour les articles
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = ArticleService.get_markdown_list()
    if result and result['success'] == True:
        return JSONResponse({'success': 'Markdown list', 'markdown_list': result['markdowns']}, status_code=200)
    return JSONResponse({'error': 'Could not get the markdown list'}, status_code=400)

@router.post('/tuto/create_markdown', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=create_markdown_responses)
async def create_markdown(r: Request, markdown: CreateMarkdownModel, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Créer un markdown pour les tutoriels
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = TutorialService.create_markdown(markdown.name, markdown.content)
    if result and result['success'] == True:
        return JSONResponse({'success': f'Markdown "{markdown.name}" created', 'markdown_url': result}, status_code=200)
    return JSONResponse({'error': 'Could not create the markdown'}, status_code=400)


@router.get('/tuto/available_markdown', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=available_markdown_responses)
async def get_tuto_available_markdown(r: Request, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Récupérer les markdowns disponibles pour les tutoriels
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = TutorialService.get_markdown_list()
    if result and result['success'] == True:
        return JSONResponse({'success': 'Markdown list', 'markdown_list': result['markdowns']}, status_code=200)
    return JSONResponse({'error': 'Could not get the markdown list'}, status_code=400)

@router.post('/path/add', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=create_markdown_responses)
async def add_path(r: Request, name: str, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Ajouter un chemin
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = TutorialService.create_path(name)

    if result == True:
        return JSONResponse({'success': 'Path created', 'path': name}, status_code=200)
    return JSONResponse({'error': 'Could not create the path'}, status_code=400)

@router.patch('/path/update', tags=['admin'], dependencies=[Depends(AdminChecker(2))])
async def update_path(r: Request, id: int, new_name: str, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Modifier un chemin
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = TutorialService.update_path(new_name, id)

    if result:
        return JSONResponse({'success': 'Path updated', 'path': result['path']}, status_code=200)
    return JSONResponse({'error': 'Could not update the path'}, status_code=400)

@router.delete('/path/delete', tags=['admin'], dependencies=[Depends(AdminChecker(2))])
async def delete_path(r: Request, id: int, credentials: str = Depends(AdminChecker(2))) -> JSONResponse:
    """
    Supprimer un chemin
    """
    Log.route_log(r, "moderation routes", JWT.decodeJWT(credentials)["uuid"])
    result = TutorialService.delete_path(id)

    if result == True:
        return JSONResponse({'success': 'Path deleted'}, status_code=200)
    return JSONResponse({'error': 'Could not delete the path'}, status_code=400)