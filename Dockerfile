FROM docker.io/python:3.12-slim
ARG APP_NAME
ARG APP_VERSION
RUN pip install --no-cache ${APP_NAME}==$(echo ${APP_VERSION} | cut -c 2-)
ENTRYPOINT [ "${APP_NAME}" ]
