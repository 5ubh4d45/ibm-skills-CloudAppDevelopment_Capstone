FROM python:3.11.4-bookworm

ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

RUN apt-get update && apt-get install -y netcat-traditional

ENV APP_HOME=/app

RUN mkdir $APP_HOME

WORKDIR $APP_HOME

COPY ./requirements.txt $APP_HOME/requirements.txt

RUN pip install -r requirements.txt

COPY . $APP_HOME

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

CMD [ "gunicorn", "--bind", ":8000", "--workers", "3",  "djangobackend.wsgi" ]