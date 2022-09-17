from fastapi import APIRouter, Depends
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
from models.response.TutorialResponseModel import TutorialResponseModel
from models.response.UnbanResponseModel import UnbanResponseModel
from models.response.BanListResponseModel import BanListResponseModel
from models.input.IdModel import IdModel
from services.article import ArticleService
from services.moderation import ModerationService
from services.tutorial import TutorialService
from starlette.responses import JSONResponse
from services.utils.AdminChecker import AdminChecker
from services.utils.JWT import JWT
from services.utils.JWTChecker import JWTChecker

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

@router.get('/banlist/{uuid}', dependencies=[Depends(AdminChecker(1))], tags=['moderation'], responses=banlist_responses)
async def get_banlist(uuid: str):
    datas = ModerationService.get_banlist(uuid)
    return JSONResponse({"data": datas})

@router.post('/ban', dependencies=[Depends(AdminChecker(1))], tags=['moderation'], responses=ban_responses)
async def ban(ban_model: BanModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if ban_model.uuid == None:
        return JSONResponse({"error": "UUID not provided"}, status_code=400)
    else:
        is_banned = ModerationService.ban(ban_model.uuid, jwt['uuid'], ban_model.reason, ban_model.expires)
        if is_banned:
            return JSONResponse({"uuid": ban_model.uuid, "banned_by": jwt['uuid'], "reason": ban_model.reason, "expires": ban_model.expires})
        else:
            return JSONResponse({"error": "Cannot ban this user"}, status_code=400)

@router.post('/unban', dependencies=[Depends(AdminChecker(1))], tags=['moderation'], responses=unban_responses)
async def unban(revoke: UnbanModel, credentials: str = Depends(JWTChecker())):
    jwt = JWT.decodeJWT(credentials)
    if revoke.uuid == None:
        return JSONResponse({"error": "UUID not provided"}, status_code=400)
    else:
        is_unbanned = ModerationService.unban(revoke.uuid, jwt['uuid'], revoke.reason)
        if is_unbanned:
            return JSONResponse({"uuid": revoke.uuid, "revoked_by": jwt['uuid'], "reason": revoke.reason})
        else:
            return JSONResponse({"error": "Cannot unban this user"}, status_code=400)

@router.post('/mod', dependencies=[Depends(AdminChecker(2))], tags=['admin'])
async def set_mod(mod_model: ModModel):
    if mod_model.uuid == None:
        return JSONResponse({"error": "UUID not provided"}, status_code=400)
    else:
        is_changed = ModerationService.set_mod(mod_model.uuid, mod_model.role)
        if is_changed:
            return JSONResponse({"uuid": mod_model.uuid, "role": mod_model.role})
        else:
            return JSONResponse({"error": "Cannot change mod role of this user"}, status_code=400)

@router.post('/tuto/create', dependencies=[Depends(AdminChecker(2))], tags=['admin'], responses=create_tutorial_responses)
async def create_tutorial(tutorial_model: TutorialModel):
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
    result = TutorialService.create_tutorial(tutorial_model.title, tutorial_model.markdownUrl, tutorial_model.startCode, tutorial_model.category, tutorial_model.answer, tutorial_model.shouldBeCheck)
    if result:
        return JSONResponse({"success": "Tutorial created !"})
    else:
        return JSONResponse({"error": "This tutorial already exists"}, status_code=400)

@router.patch('/tuto/update', dependencies=[Depends(AdminChecker(2))], tags=['admin'], responses=update_tutorial_responses)
async def edit_tutorial(tutorial_model: TutorialEditModel):
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
    result = TutorialService.update_tutorial(tutorial_model.id, tutorial_model.title, tutorial_model.markdownUrl, tutorial_model.category, tutorial_model.answer, tutorial_model.startCode, tutorial_model.shouldBeCheck)
    if result:
        return JSONResponse({'success': 'Updated tutorial !'})
    else:
        return JSONResponse({'error': 'Can\'t update tutorial'}, status_code=400)

@router.patch('/tuto/toggle', dependencies=[Depends(AdminChecker(2))], tags=['admin'], responses=toggle_tutorial_responses)
async def enable_disable_tutorial(id_model: IdModel):
    if id_model.id == None:
        return JSONResponse({'error': 'Tutorial ID not provided'}, status_code=400)
    tutorial = TutorialService.get_tutorial(id_model.id)
    enabled = tutorial.get('enabled')
    enabled = not enabled
    result = TutorialService.toggle_tutorial(id_model.id, enabled)
    if result:
        return JSONResponse(result)
    return JSONResponse({'error': 'Can\'t toggle this tutorial'}, status_code=400)

@router.post('/category/create', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=create_category_responses)
async def create_category(category: CategoryModel):
    result = TutorialService.create_category(category.name, category.description, category.image)
    if result:
        return JSONResponse({'success': 'Created category ' + category.name})
    return JSONResponse({'error': 'Could not create the category'}, status_code=400)

@router.patch('/category/update', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=update_category_responses)
async def update_category(category: CategoryModel):
    result = TutorialService.update_category(category.name, category.description, category.image)
    if result:
        return JSONResponse({'success': 'Updated category ' + category.name})
    return JSONResponse({'error': 'Could not update the category'}, status_code=400)

@router.delete('/category/delete', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=delete_category_responses)
async def delete_category(name: CategoryNameModel):
    result = TutorialService.delete_category(name.name)
    if result:
        return JSONResponse({'success': 'Category deleted'})
    return JSONResponse({'error': 'Could not delete the category'}, status_code=400)

@router.post('/article/create_markdown', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=create_markdown_responses)
async def create_markdown(markdown: CreateMarkdownModel):
    print(f'markdown: {markdown}', flush=True)
    result = ArticleService.create_markdown(markdown.name, markdown.content)
    if result and result['success'] == True:
        return JSONResponse({'success': f'Markdown "{markdown.name}" created', 'markdown_url': result})
    return JSONResponse({'error': 'Could not create the markdown'}, status_code=400)

# @router.get('/article/available_markdown', tags=['admin'], dependencies=[Depends(AdminChecker(2))], responses=available_markdown_responses)
# async def get_available_markdown():
#     result = ArticleService.get_markdown_list()
#     if result and result['success'] == True:
#         return JSONResponse({'success': 'Markdown list', 'markdown_list': result['markdowns']})
#     return JSONResponse({'error': 'Could not get the markdown list'}, status_code=400)
