pip install -r requirements.txt
echo 'Checking database...'
bash scripts/update_db.sh
echo 'Starting server...'
cd src && uvicorn main:app --reload --host=0.0.0.0 --port=8080