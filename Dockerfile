FROM python:3

RUN pip install --upgrade pip && \
    pip install \
    black \
    mutmut \
    numpy \
    pandas \
    scipy \
    lmfit \
    pytest==5.0.1

WORKDIR /workdir
