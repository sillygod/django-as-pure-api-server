FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN \
  apt-get update && \
  apt-get install -y apt-transport-https && \
  apt-get clean && \
  mkdir app

ADD . /app/

WORKDIR /app
RUN pip install -r requirements/dev.txt && pip install uwsgi

RUN useradd -ms /bin/bash jing

RUN \
  python manage.py collectstatic --noinput

EXPOSE 8000
ENV PORT 8000

# https://docs.docker.com/engine/reference/builder/
# According to the doc, we can use the exec form of ENTRYPOINT to set fairly stable default
# commands and arguments.
# ex.
# ENTRYPOINT ["top", "-b"]
# CMD ["-c"]

ENTRYPOINT ["/app/compose/entrypoint.sh"]
CMD ["uwsgi --ini core/wsgi/uwsgi.ini"]
