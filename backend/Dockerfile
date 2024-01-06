FROM python:3.11.2

LABEL maintainer="aliaghdam.erfan@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY run.sh /scripts/run.sh

EXPOSE 8000

ARG DEV=false

RUN python -m venv /py

RUN /py/bin/pip install --upgrade pip

RUN apt-get update && apt-get install -y postgresql-client

RUN /py/bin/pip install -r /tmp/requirements.txt --use-pep517

RUN if [ $DEV = "true" ]; \
      then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi

RUN adduser --disabled-password --no-create-home django-user

RUN rm -rf /tmp

COPY . .

RUN chmod -R +x /scripts

RUN chown -R django-user:django-user /scripts

RUN chown -R django-user:django-user .

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]