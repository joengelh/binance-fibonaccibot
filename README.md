## Introduction
Just a fun exercise to see if fibonacci retracement levels and linear regression predicts the value of cryptocurrencies to one antoher. Have fun =) 

## Architecture

![architecture](https://user-images.githubusercontent.com/73387330/118108067-d6567000-b3df-11eb-8ad4-33075a3a6499.PNG)

The Trading bot comes as a microservices architecture launched via docker-compose.
Docker compose can be installed using the ansible Role 
[go to github](https://github.com/joengelh/ansible-kvm/tree/main/roles/docker-compose)

## Preparation

After cloning the repository from GitHub using ``git clone https://github.com/joengelh/binance-fibonaccibot.git`` copy the .env.sample file to .env and fill in your information.

apiKey=YOUR_API_KEY        = your binance api key
apiSecret=YOUR_API_SECRET  = your binance api secret
dbName=postgres            = set to preferences or leave default
dbUser=postgres            = set to preferences or leave default
POSTGRES_PASSWORD=password = set to preferences or leave default
dbHost=localhost           = set to preferences or leave default
dbPort=5432                = set to preferences or leave default
liveTrading=false          = enable or disable live trading, while the backtesting method is not as accurate
liveVolume=1               = ammount of BNB used per signal

Thereafter the service can be started using ``docker-compose up -d --build``
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
fibonacci-crawler|trading logic||
fibonacci-validator|profit calculator||
fibonacci-webui|result display|13000|

# Tools
for monitoring the RScripts:
* ``fibLvlValidator.R``
![grafik](https://user-images.githubusercontent.com/73387330/116047661-991a8000-a674-11eb-92c0-c537bc145512.png)

* ``plotValidator.R``

![grafik](https://user-images.githubusercontent.com/73387330/116047232-290bfa00-a674-11eb-9be0-ca638d47aed4.png)

can be used.

