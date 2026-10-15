FROM python:3.12-alpine AS builder

WORKDIR /src

COPY requirements.txt .

RUN pip install --upgrade pip && pip wheel --wheel-dir /wheels -r requirements.txt



FROM python:3.12-alpine

ARG LAB_LOGIN
ARG LAB_TOKEN

LABEL org.lab.login="$LAB_LOGIN"
LABEL org.lab.token="$LAB_TOKEN"

ENV LAB_LOGIN=$LAB_LOGIN
ENV LAB_TOKEN=$LAB_TOKEN
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser -D -u 10001 appuser

COPY --chown=appuser:appuser --from=builder /wheels /wheels
COPY --chown=appuser:appuser requirements.txt .

RUN pip install --no-index --find-links=/wheels -r requirements.txt

COPY --chown=appuser:appuser app/ .

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--graceful-timeout", "10", "--worker-tmp-dir", "/dev/shm", "app:app"]
