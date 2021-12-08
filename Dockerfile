# Pull base image
FROM python:3.9.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code
# ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# Install dependencies
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml /code/
RUN poetry install --no-dev


# Copy project
COPY . /code/
