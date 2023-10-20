FROM python:3.11

WORKDIR /users-ms

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY wait-for-it.sh /users-ms/

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app","--host","0.0.0.0","--port","8000"]
