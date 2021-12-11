# Single fat docker build for the application
# Use alpine as the base version and add the following
# [1] Python
# [2] Java (JRE and JDK)
# [3] Python Dependencies
# [4] NPM and Node

# Stage [0] : Alpine Checkout
FROM alpine:3

ARG host
ENV HOST=$host

##################### INSTALL DEPENDENCIES #################################

RUN apk update && apk add bash

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turn off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install Python and PIP
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Install Java (JDK)
RUN apk add --update --no-cache openjdk8


# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
ENV PATH="$JAVA_HOME/bin:${PATH}"

RUN export JAVA_HOME

# Install NODE
RUN apk add --update nodejs npm

######################## APPLICATION INSTALL ##############################

# Application Checkout
RUN mkdir -p /nexus
COPY . /nexus

# Start the UI build
WORKDIR /nexus/src/client
RUN echo "REACT_APP_SERVER=\"http://${HOST}/api\"" > .env
RUN npm run deploy

# Start the Python Assembly
WORKDIR /nexus

# Set open ports for the application
EXPOSE 5000

######################## PROCESS RUNNER ##################################

RUN python -m pip install -r requirements.txt
CMD python -m src.app -s 0.0.0.0 -p 5000
