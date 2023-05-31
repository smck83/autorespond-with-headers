FROM python:3
LABEL maintainer="s@mck.la"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ntp \
    && mkdir -p /opt/autoresponder-with-headers/
RUN pip install mail-parser
ADD main.py /opt/autoresponder-with-headers/
#RUN pip3 install 
WORKDIR /opt/autoresponder-with-headers/


VOLUME ["/opt/autoresponder-with-headers"]

ENTRYPOINT python -u /opt/autoresponder-with-headers/main.py

