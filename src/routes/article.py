from fastapi import APIRouter

router = APIRouter(prefix='/article')

@router.get('/all', tags=['article'])
async def get_all_articles():
    pass

@router.get('/id/{id}', tags=['article'])
async def get_article(id: int):
    pass

@router.post('/create', tags=['article'])
async def create_article():
    pass

@router.patch('/update', tags=['article'])
async def update_article():
    pass

@router.delete('/delete', tags=['article'])
async def delete_article():
    pass