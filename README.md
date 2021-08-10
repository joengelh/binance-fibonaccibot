# Introduction
Just a fun exercise to see if fibonacci retracement levels and simple correlation can predict the value of cryptocurrencies to one antoher. Have fun =) 


# Architecture

![Architecture](https://user-images.githubusercontent.com/73387330/126828603-6acc27bc-b959-472e-a22a-51606a5e77f8.PNG)

The Trading bot comes as a microservices architecture launched via docker-compose.
Docker compose can be installed using the ansible Role 
[go to github](https://github.com/joengelh/ansible-kvm/tree/main/roles/docker-compose)


# Preparation

After cloning the repository from GitHub using ``git clone https://github.com/joengelh/binance-fibonaccibot.git`` copy the .env.sample file to .env and fill in your information.

```bash
apiKey                     = your binance api key
apiSecret                  = your binance api secret
dbName                     = set to preferences or leave default
dbUser                     = set to preferences or leave default
dbTable                    = set to preferences or leave default
POSTGRES_PASSWORD          = set to preferences or leave default
dbHost                     = set to preferences or leave default
dbPort                     = set to preferences or leave default
liveTrading                = enable or disable live trading, while the backtesting method is not as accurate
liveVolume                 = amount of base currency used per signal
botToken                   = telegram bot token, given by the bot father
baseCurrency               = base currency to grow
```

Thereafter the service can be started using ``docker-compose up -d --build``
and stopped using ``docker-compose down``.

# Components

 The bot consists of the following components:

Component|Function|Ports|Volumes
---|---|---|---
fibonacci-db|postgres database|5432|/private/db:/var/lib/postgresql/data:rw<br>./container-db/initdb.d:/docker-entrypoint-initdb.d
fibonacci-validator|profit calculator||
fibonacci-webui|result display|13000|
fibonacci-cache|redis database|6379|
fibonacci-predictor|calculating present trades performance||
fobonacci-telegram|can use bot to give live performance overview||

# Webui

The Webui Displays Information about the Bot´s performance.

![webui](https://user-images.githubusercontent.com/73387330/126384015-8535dc64-af3d-4b0a-95ec-0a6a2b36955b.PNG)

* <strong>Free Spot</strong> gives an information about how buch selected base currency is still available to open more positions.
* <strong>Open Trades</strong> displays the amount of trades opened and not closed yet.
* <strong>Sum Result</strong> can either show how much base currency has been earned yet in live mode or how many percent growth based on the selected volume has been gained, taking the markets spread and trading fees, aswell as market movements into account.
* <strong>24h Sum Result</strong> can either show how much base currency has been earned in the past 24h in live mode or how many percent growth based on the selected volume has been gained, taking the markets spread and trading fees, aswell as market movements into account.
* <strong>Simulated Avg</strong> shows by how many percent points all open positions are in profit/loss when they would be closed immediately.
* <strong>Simulated Sum</strong> shows how much base currency would be earned if all open positions would be closed immediately.
* <strong>Simulated Winners</strong> counts the open positions in profit at the moment.
* <strong>Simulated Losers</strong> counts the open positions out of profit at the moment.


# Tools
for monitoring the RScripts:
* ``fibLvlValidator.R``
![grafik](https://user-images.githubusercontent.com/73387330/116047661-991a8000-a674-11eb-92c0-c537bc145512.png)

* ``plotValidator.R``

![grafik](https://user-images.githubusercontent.com/73387330/116047232-290bfa00-a674-11eb-9be0-ca638d47aed4.png)

can be used.


# backup & restore

## backup

```bash
sudo docker exec -i fibonacci-db /bin/bash -c "PGPASSWORD=password pg_dump --username postgres postgres" > dump.sql
```

The backup process can also be automated using the Ansible Role: <strong>cron-place</strong>.

## restore

```bash
sudo docker-compose up -d db
sudo docker exec -i fibonacci-db /bin/bash -c "PGPASSWORD=password psql --username postgres postgres" < dump.sql
sudo docker-compose up -d
```
