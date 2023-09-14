# Text improvement engine

## Prerequisites

Install Docker:
```
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Run Docker containter
Docker build:

```
bash build.sh
```

Run containter:

```
bash run.sh
```

## API
For ease of visualization, use swagger UI http://0.0.0.0:8000/docs

 - POST /api/v1/upload_terms/    - upload new standardised terms in csv format

 - POST /api/v1/text_improvement - send text and get improvement suggestions as response as png (made specificaly only for visualising)

## BASIC USAGE EXAMPLE
Open swagger UI http://0.0.0.0:8000/docs

![Screenshot from 2023-09-14 12-35-22](https://github.com/vasilenkone/text_improvement_engine/assets/86557038/723333a6-0682-455c-811f-91aadd8e1ca0)

Press 'Try it out' button near /api/v1/text_improvement

![Screenshot from 2023-09-14 12-36-11](https://github.com/vasilenkone/text_improvement_engine/assets/86557038/b3475bcb-505b-4999-86da-e1e17d100c9f)

Insert your text in Check field and press 'Execute' and wait for response (some time for downloading model files is needed)

![Screenshot from 2023-09-14 13-18-47](https://github.com/vasilenkone/text_improvement_engine/assets/86557038/39fc3f14-5f34-49ea-98a7-62e2aa9ffa62)


The result shown as a picture. In the left part you can see improvement suggestions for group of words, and in the right part suggestions for the sentences

## STACK AND TECHNOLOGIES USED

Python libs
```
dataframe-image
matplotlib==3.7.3 
nltk==3.8.1
pandas==1.5.3
python-multipart==0.0.6
sentence-transformers==2.2.2
fastapi==0.101.1
uvicorn==0.23.2
```
Docker - for isolating enviroment and quick project starting

FastAPI server for API to send requests, get responces and using swagger ui for visualising (since there were the visualisation requirement)

Model:
- text preprocessing using NLTK word and sentence tokenizing (since we get different useful suggestions for words and sentences)
- words/sentences embeddings using SentenceTransformers - framework for state-of-the-art sentence, text and image embeddings
- pretrained model "all-MiniLM-L12-v2" used in SentenceTransformers framework. It's not the best performance model in the top list, but it shows not bad results for this particular task.
- List of available models (easy to change): https://www.sbert.net/docs/pretrained_models.html


