# hirespy

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/item084/hirespy)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Hi-Res server python program. **"HIRE SPY"!**

```sh
$ python3 -m venv env
$ echo $PYTHONPATH
$ unset PYTHONPATH
$ source env/bin/activate
$ pip install --upgrade pip setuptools wheel
$ pip install -e .
$ export FLASK_DEBUG=True
$ export FLASK_APP=hirespy
$ export HIRESPY_SETTINGS=config.py
$ flask run --host 0.0.0.0 --port 8000
$ export LC_ALL=en_US.UTF-8
$
$ pkill -f gunicorn
$ pkill -f nucleserver
$ bin/hirespydb reset
$ gunicorn -b localhost:8000 -w 1 -D hirespy:app
```

# Todo list
- UI
- metadata
- usable for ML
- Keras not thread safe, add concurrency

# Hi-Res Project Server

This is a manual for setting up a server for **Hi-Res Project** on **Linux** system. The server has two main functions:
 - Host local data and serve to the **Nucleome Browser** ([nucleome browser](https://vis.nucleome.org/)).
- Host a website. Receive data from client, process the data with **Python** and send back a data server url.

## Data Server

- Use a server program ([nucleserver](https://github.com/nucleome/nucleserver)) provided by **Nucleome Browser**.
- Use reverse proxy by **Nginx**.

## Main Data Set

The main dataset is stored on the disk and served up to the **Nucleome Browser** by a **nucleserver** process. It can be accessed by the link to the browser ([N/A]()).

### Setup
 - nucleserver :
	 - static xslx sheet
 - reverse proxy by **nginx** : 
	 - static ip
	 - domain
	 - SSL certification by **certbot**

## Generated Data Set

19 tracks per user.

### Setup
 - website (in progress) :
	 - probably javascipt 
 - python (in progress) : 
	 - generate 19 tracks
	 - generate a xslx sheet 
 - nucleserver :
	 - capacity (?)
	 - life cycle (?)
 -  reverse proxy by **nginx** : 
	 - regex match, e.g. https://data.website.com/port/8000/path -> https://data.website.com:8000/path 

## Google doc

```sh
$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## nginx config

/etc/nginx/default.d/proxy.conf
pkexec systemctl (restart|stop|start|status) nginx

### to proxy remote to a localhost

```
http {
  server {
    listen 127.0.0.1:8888;
        location / {
        proxy_pass https://nucleome.dcmb.med.umich.edu;
        }
  }
}
```

## json

/config/


## acronym
AD adrenal gland
HC hippocampus
LG lung
LV liver
PA pancreas
SB small bowel
SX spleen
OV ovary
IMR90
GM12878

# Issues

## 5.18

- tutorial updated

- feng fan no progress [x] [x]
    - cannot finish reset part of different tissue
    - limit to chr7, tutorial not updated completely
    - but `structure` is ready

- command line tool

- sqlite concurrency
    - trying to switch to Mysql

- module independency
    - split functions
    - direction 没有方向 do best for current purpose
 
- model cocurrency
    - still need to be fixed, with model developer

- other implementation details [x]

- write a manual [x]

- Nucleic Acid Research
    - mostly focus on contents
    - do more research [x]

## Database

- Mysql
    - SHOW DATABASES;
    - CREATE DATABASE hirespy;
    - USE hirespy;
    - SHOW TABLES;
