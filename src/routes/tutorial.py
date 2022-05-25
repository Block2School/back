from fastapi import APIRouter

router = APIRouter(prefix='/tuto')

@router.get('/all')
async def get_all_tutorials():
    pass

@router.get('/{id}')
async def get_tutorial(id: int):
    pass

@router.get('/category/{category}')
async def get_all_tutorials_by_category():
    pass

@router.get('/scoreboard/{id}')
async def get_scoreboard_tutorial(id: int):
    pass

@router.get('/success/{id}')
async def get_success_percentage_tutorial(id: int):
    pass

@router.get('/scoreboard/me')
async def get_user_all_score():
    pass

@router.get('/scoreboard/me/{id}')
async def get_user_score_tutorial():
    pass

@router.get('/success/me')
async def get_user_success_tutorials():
    pass

@router.post('/complete')
async def complete_tutorial():
    pass