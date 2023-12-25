FROM python:3.10
LABEL authors="spacewalrus"
WORKDIR /Django_Stripe

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]