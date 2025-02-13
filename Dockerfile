FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0", "-w", "4", "main:app"]
