## Introduction
Just a fun exercise to see if fibonacci retracement levels and linear regression predicts the value of cryptocurrencies to one antoher. Have fun =) 

## Architecture
The Trading bot comes as a microservices architecture launched via docker-compose.
Docker compose can be installed using the ansible Role 
[go to github](https://github.com/joengelh/ansible-kvm/tree/main/roles/docker-compose)

## Preparation
After copying the .env.sample to .env and filling it with your details,
the service can be started using ``docker-compose up -d --build``
and stopped using ``docker-compose down``.

# Used Ressources
The open source repository binance python profit
[go to github](https://github.com/UPetit/python-binance-profit)
is used in the crawler microservice.

```bash
.
├── app
│   ├── client.py
│   ├── entities.py
│   ├── object_values
│   │   ├── args.py
│   │   ├── base.py
│   │   ├── filters.py
│   │   ├── orders.py
│   │   ├── __pycache__
│   │   │   ├── args.cpython-38.pyc
│   │   │   ├── base.cpython-38.pyc
│   │   │   ├── filters.cpython-38.pyc
│   │   │   ├── orders.cpython-38.pyc
│   │   │   └── symbol.cpython-38.pyc
│   │   └── symbol.py
│   ├── __pycache__
│   │   ├── client.cpython-38.pyc
│   │   ├── entities.cpython-38.pyc
│   │   └── tools.cpython-38.pyc
│   └── tools.py
└── crawler.py
```

## Components

 The bot consists of the following components:

Component|Function|Ports|Volumes
---|---|---|---
fibonacci-db|timescale database|5432|fibonacci-volume
fibonacci-crawler |trading logic||
fibonacci-validator|profit calculator||

# Tools
for monitoring the RScripts:
* ``fibLvlValidator.R``
* ``plotValidator.R``

can be used.


