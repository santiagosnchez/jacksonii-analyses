FROM community.wave.seqera.io/library/python:3.12.2--a1e8cc3506a889da
COPY . /workspace
WORKDIR /workspace
RUN apt-get update && apt-get install -y git
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN python -m ipykernel install --user --name jacksonii_analyses --display-name "Python (jacksonii)"