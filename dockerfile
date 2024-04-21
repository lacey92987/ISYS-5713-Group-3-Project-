FROM python:3.8-slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
COPY database.db /app/database.db


EXPOSE 80

CMD ["python", "frontend_dash.py"]


