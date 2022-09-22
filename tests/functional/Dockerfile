FROM python:3.10

WORKDIR /opt/app/tests/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . ./functional/
COPY __init__.py ./

ENTRYPOINT ["pytest", "./functional/src"]
#CMD ["python3", "-m", "http.server", "8000"]
