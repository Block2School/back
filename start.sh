pip3 install -r requirements.txt
echo 'Checking database...'
bash scripts/update_db.sh
echo 'Starting server...'
cd src && uvicorn main:app --reload --port=8080