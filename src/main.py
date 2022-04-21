from fastapi import FastAPI, Depends
import routes.login as LoginRoute
from services.JWTChecker import JWTChecker
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

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

@app.get("/", dependencies=[Depends(JWTChecker())], tags=['root'])
def read_root():
    return {"hello": 'world'}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)