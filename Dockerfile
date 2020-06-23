FROM python:3

RUN pip install --upgrade pip && pip install \
    black \
    flake8 \
    lmfit \
    mutmut \
    numpy \
    pandas \
    pytest-cov \
    pytest==5.0.1 \
    scipy

WORKDIR /workdir
