FROM python:3.9
EXPOSE 8080

WORKDIR /app
COPY . .
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["chainlit", "run", "main.py", "-h", "--port", "8080"]  
