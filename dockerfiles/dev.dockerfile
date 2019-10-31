FROM python:3.7-alpine as builder
ENV PYTHONUNBUFFERED 1

RUN apk update && \
  apk add --no-cache curl build-base gcc jpeg-dev zlib-dev git postgresql-dev linux-headers musl-dev
COPY requirements /app/requirements
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r /app/requirements/dev.txt

FROM python:3.7-alpine
RUN apk add --no-cache jpeg-dev zlib-dev
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
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
