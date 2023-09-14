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
1. Docker build:

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

