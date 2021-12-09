# Pull base image
FROM python:3.9.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code
# Set pythonpath for celery
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Install dependencies
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml /code/
RUN poetry install --no-dev

# Copy project
COPY ./spam_recycler /code/

# Install supervisor
RUN apt-get update && apt-get install supervisor -y

# Install spamd
RUN apt-get install spamassassin -y