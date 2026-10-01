FROM python:3.12-slim
WORKDIR /srv
COPY integration-bridge/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/srv/integration-bridge PHOTO_DIR=/data/photos PYTHONUNBUFFERED=1
RUN mkdir -p /data/photos
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request,os;urllib.request.urlopen('http://localhost:'+os.getenv('PORT','8000')+'/health')"
CMD ["sh","-c","uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
