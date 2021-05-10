// import modules
require('dotenv').config()
const { Client } = require('pg')
const express = require('express');
const Binance = require('node-binance-api');
const app = express();

// serve static index.html
app.listen(13000, () => console.log('listening on port 13000'));
app.use(express.static('../public'));

// load binance connection vars from environment
const binance = new Binance().options({
	  APIKEY: process.env.apiKey,
	  APISECRET: process.env.apiSecret
});

// get current BNB balance from account
app.get('/assets', (request, response) => {
	binance.balance((error, balances) => {
	    if ( error ) return console.error(error);
	    console.log("BNB balance: ", balances.BNB.available);
	    response.json(balances.BNB.available)
	});
});

// load databse connection vars from environment
const client = new Client({
	  user: process.env.dbUser,
	  host: process.env.dbHost,
	  database: process.env.dbName,
	  password: process.env.POSTGRES_PASSWORD,
	  port: process.env.dbPort,
})

// query database for open trades
client.connect()
client.query('SELECT * from table001 where takeprofit is not null and resultpercent is null;', (err, res) => {
	  console.log(res.rowCount)
	  const openTrades = res.rowCount;
	  client.end()
})

