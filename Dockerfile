FROM python:3.11-slim

# نصب ابزارهای لازم برای کامپایل پکیج‌ها
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# دانلود فایل wait-for-it
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /usr/local/bin/wait-for-it \
  && chmod +x /usr/local/bin/wait-for-it



WORKDIR /src

COPY requirements.txt .


RUN pip install --no-cache-dir --retries 10 -r requirements.txt



COPY . .


EXPOSE 8000



CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
