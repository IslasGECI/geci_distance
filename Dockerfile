FROM python:3
WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    flake8 \
    lmfit \
    mutmut \
    numpy \
    pandas \
    pylint \
    pytest-cov \
    pytest==5.0.1 \
    scipy
