# Отчет по лабораторной 2.
**Цель работы:** собрать production-образ для мини-сервиса на Flask так, чтобы он был:
- маленький (**< 150 MB**),
- безопасный (**не root**),
- с **HEALTHCHECK**,
- корректно завершался по **SIGTERM**,
- умел работать при `--read-only`,
- принимал конфиг через переменные окружения **без пересборки**.
---
## Вывод docker history

```bash
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
0f77ca5fa282   44 minutes ago   CMD ["gunicorn" "-b" "0.0.0.0:8000" "--grace…   0B        buildkit.dockerfile.v0
<missing>      44 minutes ago   EXPOSE [8000/tcp]                               0B        buildkit.dockerfile.v0
<missing>      44 minutes ago   HEALTHCHECK {Test:[CMD-SHELL python3 -c "imp…   0B        buildkit.dockerfile.v0
<missing>      44 minutes ago   USER appuser                                    0B        buildkit.dockerfile.v0
<missing>      44 minutes ago   COPY --chown=appuser:appuser app/ . # buildk…   12.3kB    buildkit.dockerfile.v0
<missing>      44 minutes ago   RUN |2 LAB_LOGIN=scr1mer228 LAB_TOKEN=b966a0…   7.62MB    buildkit.dockerfile.v0
<missing>      44 minutes ago   COPY --chown=appuser:appuser requirements.tx…   12.3kB    buildkit.dockerfile.v0
<missing>      44 minutes ago   COPY --chown=appuser:appuser /wheels /wheels…   872kB     buildkit.dockerfile.v0
<missing>      44 minutes ago   RUN |2 LAB_LOGIN=scr1mer228 LAB_TOKEN=b966a0…   41kB      buildkit.dockerfile.v0
<missing>      45 hours ago     WORKDIR /app                                    8.19kB    buildkit.dockerfile.v0
<missing>      45 hours ago     ENV PYTHONUNBUFFERED=1                          0B        buildkit.dockerfile.v0
<missing>      45 hours ago     ENV PYTHONDONTWRITEBYTECODE=1                   0B        buildkit.dockerfile.v0
<missing>      45 hours ago     ENV LAB_TOKEN=b966a086718bb9e6d20f4a1927f4bd…   0B        buildkit.dockerfile.v0
<missing>      45 hours ago     ENV LAB_LOGIN=scr1mer228                        0B        buildkit.dockerfile.v0
<missing>      45 hours ago     LABEL org.lab.token=b966a086718bb9e6d20f4a19…   0B        buildkit.dockerfile.v0
<missing>      45 hours ago     LABEL org.lab.login=scr1mer228                  0B        buildkit.dockerfile.v0
<missing>      45 hours ago     ARG LAB_TOKEN=b966a086718bb9e6d20f4a1927f4bd…   0B        buildkit.dockerfile.v0
<missing>      45 hours ago     ARG LAB_LOGIN=scr1mer228                        0B        buildkit.dockerfile.v0
<missing>      13 days ago      CMD ["python3"]                                 0B        buildkit.dockerfile.v0
<missing>      13 days ago      RUN /bin/sh -c set -eux;  for src in idle3 p…   16.4kB    buildkit.dockerfile.v0
<missing>      13 days ago      RUN /bin/sh -c set -eux;   apk add --no-cach…   50.4MB    buildkit.dockerfile.v0
<missing>      13 days ago      ENV PYTHON_SHA256=c2c4321961fab0fb999d66e0ce…   0B        buildkit.dockerfile.v0
<missing>      13 days ago      ENV PYTHON_VERSION=3.12.15                      0B        buildkit.dockerfile.v0
<missing>      13 days ago      ENV GPG_KEY=7169605F62C751356D054A26A821E680…   0B        buildkit.dockerfile.v0
<missing>      13 days ago      RUN /bin/sh -c set -eux;  apk add --no-cache…   2.83MB    buildkit.dockerfile.v0
<missing>      13 days ago      ENV LANG=C.UTF-8                                0B        buildkit.dockerfile.v0
<missing>      13 days ago      ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…   0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      3 weeks ago      ADD alpine-minirootfs-3.24.2-x86_64.tar.gz /…   9.08MB    buildkit.dockerfile.v0
```
---

## Плюсы моей сборки
- **Multi-stage:** зависимости собираются в builder-стадии в wheel-пакеты(не нужно компилировать заново), а в финальный образ попадают только готовые wheel и runtime, без компиляторов, кэша `pip` и лишних build-зависимостей.

- **Размер:** помимо того, что мы не тянем зависимости из build, я использую более легковесный базовый слой: python:3.12-alpine

- **Безопасность:** Приложение запускается не от root, а под отдельным пользователем `appuser` с `UID 10001`, а файлы копируются с `--chown` (задает владельца сразу в момент копирования).

- **Process manager:** используется Gunicorn с `--graceful-timeout`, что даёт production-режим и корректное завершение по `SIGTERM`.

- **HEALTHCHECK:** проверяет `GET /health` через встроенный `urllib`.

- Переменная `ROCKET_SIZE` читается из окружения, поэтому меняется без пересборки.

- **Работа в режиме ro:** `--worker-tmp-dir /dev/shm` (чтобы воркер смог писать временные файлы без проблем с режимом)
