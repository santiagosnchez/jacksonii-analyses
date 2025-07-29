FROM community.wave.seqera.io/library/iqtree_newick_utils_pip_poetry:a792bac6191623f0
COPY . /workspace
WORKDIR /workspace
RUN apt-get update && \
    apt-get install -y \
        git \
        wget \
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
        python3-rtree \
        libbz2-dev \
        liblzma-dev \
        bcftools \
        mafft 
RUN wget "https://dalexander.github.io/admixture/binaries/admixture_linux-1.3.0.tar.gz" && \
    tar zxf admixture_linux-1.3.0.tar.gz -C /usr/local/bin dist/admixture_linux-1.3.0/admixture --strip-components=2 && \
    rm admixture_linux-1.3.0.tar.gz
RUN wget "https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20250615.zip" && \
    unzip -o plink_linux_x86_64_20250615.zip -d /tmp/plink && \
    mv /tmp/plink/plink /usr/local/bin/ && \
    rm -rf /tmp/plink plink_linux_x86_64_20250615.zip
ENV PATH=${PATH}:/usr/local/bin
RUN poetry config virtualenvs.create false
RUN poetry install
RUN python -m ipykernel install --user --name jacksonii_analyses --display-name "Python (jacksonii)"