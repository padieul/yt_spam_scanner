FROM python:3.10.8

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip

# Setup hosts so that requirements can be installed
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

