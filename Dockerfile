# Instantiating the base image
FROM python:3.9-slim-buster

# Installing Linux dependencies
RUN apt-get --yes update
RUN apt-get --yes install gcc libxml2

# Installing Python dependencies
COPY dependencies/requirements.txt /
RUN pip install -r /requirements.txt

# Setting the environment variables required by AWS SageMaker
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Exposing the proper port
EXPOSE 8080

# Moving the project files from local into Docker image
COPY keys/ /opt/keys
COPY models/ /opt/models
COPY container/ /opt/program

# Setting the working directory to be "opt/program/"
WORKDIR /opt/program