FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1


RUN apk update && \
  apk add --no-cache curl build-base python-dev jpeg-dev zlib-dev git postgresql-dev linux-headers musl-dev && \
  mkdir app


ADD requirements /app/requirements
WORKDIR /app
RUN pip install --no-cache-dir -r requirements/dev.txt && pip install uwsgi


# https://docs.docker.com/engine/reference/builder/
# According to the doc, we can use the exec form of ENTRYPOINT to set fairly stable default
# commands and arguments.
# ex.
# ENTRYPOINT ["top", "-b"]
# CMD ["-c"]

HEALTHCHECK --interval=5s --timeout=10s --start-period=5s \
  CMD curl -fs http://localhost:$PORT/health || exit 1

CMD ["uwsgi", "--ini", "core/wsgi/uwsgi.ini"]
