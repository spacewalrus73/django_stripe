FROM python:3.11.4-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}: ./app/"

RUN apt-get update

RUN pip install --upgrade pip

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["gunicorn", "dj_stripe.wsgi"]

#FROM python:3.10
#LABEL authors="spacewalrus"
#WORKDIR /Django_Stripe
#
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#
#COPY . .
#
#EXPOSE 8000
#
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]