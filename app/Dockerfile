FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Non-root user for industry security standard
RUN useradd -m kokuser
USER kokuser

EXPOSE 5000
CMD ["python", "app.py"]