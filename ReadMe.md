## Install docker
[Reference Doc](https://docs.docker.com/get-docker/) to install docker in machine.

## How to run project using docker
```bash
sudo docker compose up
```

## Editable content regarding to the requirements.
To display the metadata of fetching, should addd `--metadata` as param.
```bash
# ./docker-compose.yml
...
command: python fetch.py https://google.com --metadata
...
```

## How to run project without docker
### Install python 3.* in local.
### Run commands to setup python packages.
```bash
python -m pip install --no-cache-dir -r requirements.txt
```
### Run script
```bash
python fetch.py https://google.com
# or
python fetch.py https://google.com --metadata
```
### If occured error, just print the error in terminal.