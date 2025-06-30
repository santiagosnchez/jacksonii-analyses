FROM community.wave.seqera.io/library/iqtree_python_pip_poetry:0fcc8b0a840d4495
COPY . /workspace
WORKDIR /workspace
RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pyqt5 \
        python3-pyqt5.qtsvg \
        python3-pil.imagetk \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \ 
        libxext6 \
        gdal-bin \
        libgdal-dev \
        libspatialindex-dev \
        python3-pyproj \
        python3-shapely \
        python3-rtree
RUN poetry config virtualenvs.create false
RUN poetry install
RUN python -m ipykernel install --user --name jacksonii_analyses --display-name "Python (jacksonii)"