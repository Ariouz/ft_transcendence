FROM python:3.12-alpine

ARG MODE=blabla

RUN apk update
RUN apk add --no-cache bash python3 py3-pip

RUN pip3 install setuptools wheel

COPY container_scripts /scripts


RUN if [ "${MODE}" = "build" ]; then \
         ln -s /scripts/build.sh /entrypoint.sh; \
       elif [ "${MODE}" = "cleanup" ]; then \
         ln -s /scripts/cleanup.sh /entrypoint.sh; \
       else \
         echo "Invalid MODE specified: ${MODE}. Exiting."; exit 1; \
       fi

RUN chmod +x /scripts/build.sh /scripts/cleanup.sh /entrypoint.sh

RUN mkdir /libs
WORKDIR /libs

ENTRYPOINT ["bash", "/entrypoint.sh"]
