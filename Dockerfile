FROM python:3.8-slim-buster

WORKDIR /back

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install praw==3.6.0

COPY . .

CMD [ "bash", "scripts/update_db.sh", "cd src", "&&", "uvicorn main:app --reload --port=8080" ]