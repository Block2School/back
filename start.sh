pip install -r requirements.txt
echo 'Starting server...'
cd src && uvicorn main:app --reload --port=8080