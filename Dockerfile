# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY pyproject.toml poetry.lock /code/
RUN pip install poetry && poetry install

# Copy project
COPY . /code/
