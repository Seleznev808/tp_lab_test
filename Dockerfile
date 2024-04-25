FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir \
    && playwright install --with-deps

COPY . .

CMD python bot/db.py && python bot/bot.py
