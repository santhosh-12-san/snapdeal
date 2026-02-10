FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
COPY . /app/
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]