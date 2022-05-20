FROM python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app
COPY ./requirements.txt ./
COPY ./test_task ./

RUN pip install -r requirements.txt
RUN mkdir vol

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]