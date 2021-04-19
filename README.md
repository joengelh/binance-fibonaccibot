# docker-fibonacci
Bot Trading Crypto on Binance according to Fibonacci Retracement Levels.

This bot is scanning all cryptopairs on Binance for conctact of the course with the fiboancci levels within an eight hour timeperiod.
When a BNB pair reaches a level, a trade is executed and only withdrawn once the stop loss generated from the underling fibonacci level or the take profit is reached.

The bot is made from 4 microservices deployed using the docker-compose.yml in ``sudo docker-compose up -d`` in the projects root directory and can be stopped using ``sudo docker-compose down``.
The Docker Compose software on an RHEL/Centos machine can be installed using the ansible role: https://github.com/joengelh/ansible-kvm/tree/main/roles/docker-compose.

| component | function | ports | volumes |
|-----------|----------|-------|---------|
| crawler | pulls data from binance API & writes to db |   |   |
| engine | alayzes data, writes decisions to db and send API calls to trader |   |   |
| webui | display of current status and funds, on/off switch | 80  |   |
| trader | python class executing decisions over API, take profit & stop loss | 13564 |   |
| db | database storing 1 minute data and decisisons | 23450 | fibonacci-timescaledb  |

Fibonacci Levels are based on the relation of added sums to each other, the Golden Ratio. 
They occur in nature and are considered essential for esthetics.
In Daytrading, they are used to identify points of resistence/support and used to aid investment decisions.

Before running this service please fill out the .env.sample and docker-compose.yml.sample with your individual settings such as POSTGRES_PASSWORD, API_KEY or API_SECRET after renaming them to .env and docker-compose.yml respectively. 
Both of these Files are listed in the gitingore file and thus are not considered b git ad dont end up somewhere unpleasant.
