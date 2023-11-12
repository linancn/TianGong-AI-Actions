
# TianGong AI GPT Actions

## Env Preparing

### Using VSCode Dev Contariners

[Tutorial](https://code.visualstudio.com/docs/devcontainers/tutorial)

Python 3 -> Additional Options -> 3.11-bullseye -> ZSH Plugins (Last One) -> Trust @devcontainers-contrib -> Keep Defaults

Setup `venv`:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt --upgrade
```

```bash
sudo apt install python3.11-dev
sudo apt install libmagic-dev
sudo apt install poppler-utils
sudo apt install tesseract-ocr
sudo apt install libreoffice
sudo apt install pandoc
```

Install Cuda (optional):

```bash
sudo apt install nvidia-cuda-toolkit
```


## Start

```bash
uvicorn main:app --reload
```

### Auto Build

The auto build will be triggered by pushing any tag named like release-v$version. For instance, push a tag named as v0.0.1 will build a docker image of 0.0.1 version.

```bash
#list existing tags
git tag
#creat a new tag
git tag v0.0.1
#push this tag to origin
git push origin v0.0.1
```

### sphinx

```bash
sphinx-apidoc --force -o sphinx/source/ src/
sphinx-autobuild sphinx/source docs/
```

### Docker Manually Build

```bash
docker build -t linancn/tiangong-ai-actions:v0.0.1 .
docker push linancn/tiangong-ai-actions:v0.0.1
```

### Production Run

```bash

docker network create tiangongbridge

docker run --detach \
    --name nginx-proxy \
    --restart=always \
    --publish 80:80 \
    --publish 443:443 \
    --volume certs:/etc/nginx/certs \
    --volume vhost:/etc/nginx/vhost.d \
    --volume html:/usr/share/nginx/html \
    --volume /var/run/docker.sock:/tmp/docker.sock:ro \
    --network=tiangongbridge \
    --network-alias=nginx-proxy \
    nginxproxy/nginx-proxy:latest

docker run --detach \
    --name nginx-proxy-acme \
    --restart=always \
    --volumes-from nginx-proxy \
    --volume /var/run/docker.sock:/var/run/docker.sock:ro \
    --volume acme:/etc/acme.sh \
    --network=tiangongbridge \
    --network-alias=nginx-proxy-acme \
    nginxproxy/acme-companion:latest

docker run --detach \
    --name tiangong-ai-actions \
    --restart=always \
    --expose 8501 \
    --net=tiangongbridge \
    --env ui=tiangong-en \
    --env VIRTUAL_HOST=YourURL \
    --env VIRTUAL_PORT=8501 \
    --env LETSENCRYPT_HOST=YourURL \
    --env LETSENCRYPT_EMAIL=YourEmail \
    linancn/tiangong-ai-actions:latest


```

### Nginx config

default file location: /etc/nginx/sites-enabled/default

```bash
sudo apt update
sudo apt install nginx
sudo nginx
sudo nginx -s reload
sudo nginx -s stop
```

## To Do
