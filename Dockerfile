# This docker file is for the whole project

FROM python:slim

ENV PYTHONDONTWRITEBYTECODE = 1 \
    PYTHONUNBUFFERED = 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgompl
    && apt-get-clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -e .

RUN python pipeline/training_pipeline.python

# on what port the flask app should be runing
Expose 5000 

CMD ["python", "application.py"]