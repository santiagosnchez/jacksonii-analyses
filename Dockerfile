FROM community.wave.seqera.io/library/python:3.12.2--a1e8cc3506a889da
RUN apt-get update && apt-get install -y git
RUN pip install poetry
WORKDIR /workspace
COPY pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root