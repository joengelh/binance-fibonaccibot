// import modules
require('dotenv').config()
const { Client } = require('pg')
const express = require('express');
const Binance = require('node-binance-api');
const app = express();

// serve stativ index.html
app.listen(13000, () => console.log('listening on port 13000'));
app.use(express.static('../public'));

// get current BNB balance from account
const binance = new Binance().options({
	  APIKEY: process.env.apiKey,
	  APISECRET: process.env.apiSecret
});
binance.balance((error, balances) => {
	  if ( error ) return console.error(error);
	  console.info("BNB balance: ", balances.BNB.available);
});

// get ammounts of executed trades
const client = new Client({
	  user: process.env.dbUser,
	  host: process.env.dbHost,
	  database: process.env.dbName,
	  password: process.env.POSTGRES_PASSWORD,
	  port: process.env.dbPort,
})
client.connect()
client.query('SELECT * from table001 where takeprofit is not null and resultpercent is null;', (err, res) => {
	  console.log(res.rowCount)
	  const openTrades = res.rowCount;
	  client.end()
})

