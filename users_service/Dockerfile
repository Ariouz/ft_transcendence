FROM python:3.12-alpine

EXPOSE 8000/tcp

RUN mkdir /${PROJECT_NAME}
COPY . /${PROJECT_NAME}

WORKDIR "/${PROJECT_NAME}"

CMD ["sh", "setup.sh"]
