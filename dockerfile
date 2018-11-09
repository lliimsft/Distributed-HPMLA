FROM msmadl/symsgd:0.0.2

ENV MINICONDA_VERSION 4.5.11
ENV PATH /opt/miniconda/bin:$PATH
RUN apt-get update -y && \
    apt-get install -y \
        bzip2 \
        wget \
        && \
    wget -qO /tmp/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    bash /tmp/miniconda.sh -bf -p /opt/miniconda && \
    conda clean -ay && \
    rm -rf /opt/miniconda/pkgs && \
    rm /tmp/miniconda.sh && \
    find / -type d -name __pycache__ | xargs rm -rf && \
    apt-get purge -y --auto-remove bzip2 wget && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*
