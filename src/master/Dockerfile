FROM python:3.11-slim

WORKDIR /code

# install requirements
COPY . /code

RUN pip install pip --upgrade --no-cache-dir && pip install --no-cache-dir  -r /code/src/master/requirements.txt

EXPOSE 8081/tcp
EXPOSE 8081/udp

# web server
# COPY ./master_router.py /code/
# COPY ./flask_server /code/flask_server
# telegram
# COPY ./tg_router.py /code
# COPY ./telegram_server /code/telegram_server

CMD ["python", "src/master/main.py"]

ENV PYTHONPATH=./
