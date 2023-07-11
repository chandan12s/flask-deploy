FROM python:3.11

WORKDIR /app

COPY . /app

COPY venv/requirements.txt .

RUN pip install -r venv/requirements.txt

COPY . .

EXPOSE 5050

CMD ["python", "app.py"]
