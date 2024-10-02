ARG PYTHON_VERSION=3.10.14
FROM ghcr.io/mlflow/mlflow

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

COPY . .
RUN python -m pip install -r requirements.txt

EXPOSE 9292

CMD python -m mlflow server --host 0.0.0.0 --port 9292
