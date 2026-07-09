FROM python:3.10-slim

WORKDIR /app

# Kutubxonalarni requirements.txt faylisiz, toʻgʻridan-toʻgʻri oʻrnatamiz
RUN pip install --no-cache-dir flask requests

COPY . .

CMD ["python", "main.py"]

