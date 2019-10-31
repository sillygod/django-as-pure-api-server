FROM python:3.7-alpine as builder
ENV PYTHONUNBUFFERED 1

RUN apk update && \
  apk add --no-cache curl build-base jpeg-dev zlib-dev git postgresql-dev linux-headers musl-dev
COPY requirements /app/requirements
RUN pip install --install-option="--prefix=/install" --no-cache-dir -r requirements/prod.txt

FROM python:3.7-alpine
RUN apk add --no-cache jpeg-dev zlib-dev
COPY --from=builder /install /usr/local
COPY . /app

WORKDIR /app

# https://docs.docker.com/engine/reference/builder/
# According to the doc, we can use the exec form of ENTRYPOINT to set fairly stable default
# commands and arguments.
# ex.
# ENTRYPOINT ["top", "-b"]
# CMD ["-c"]

HEALTHCHECK --interval=5s --timeout=10s --start-period=5s \
  CMD curl -fs http://localhost:$PORT/health || exit 1

CMD ["uwsgi", "--ini", "core/wsgi/uwsgi.ini"]
