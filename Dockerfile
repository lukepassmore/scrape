# FROM python:3.8-alpine  # Alpine is tiny, makes for fast-booting images - python deps pre-exist
# # RUN apk update && apk add --no-cache python3 py3-pip git gcc
# # RUN yum install -y python38-{,pip,devel} build-essential git
# RUN apk add build-base # Alpine equivalent of build-essential
# COPY . /app
# WORKDIR /app
# RUN pip3 install -r requirements.txt
# ENTRYPOINT ["/usr/bin/python3", "run.py"]
FROM python
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential git
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python", "run.py"] 
