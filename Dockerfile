FROM python:3.9.12-slim-buster
RUN mkdir -p /app
WORKDIR /app
COPY . .

RUN python3 -m pip install --upgrade pip
RUN apt-get update && apt-get -y install apt-transport-https gcc ffmpeg libsm6 libxext6
RUN pip3 install -r requirements.txt
RUN python -c "import nltk; nltk.download('omw-1.4'); nltk.download('wordnet'); nltk.download('punkt'); nltk.download('stopwords')"
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]