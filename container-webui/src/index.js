// import modules
require('dotenv').config()
const { Client } = require('pg')
const express = require('express');
const Binance = require('node-binance-api');
const app = express();

// serve static index.html
app.use(function(req, res, next) {
    res.setHeader("Content-Security-Policy", "default-src *  data: blob: filesystem: about: ws: wss: 'unsafe-inline' 'unsafe-eval' 'unsafe-dynamic'; script-src * 'unsafe-inline' 'unsafe-eval'; connect-src * 'unsafe-inline'; img-src * data: blob: 'unsafe-inline'; frame-src *; style-src * data: blob: 'unsafe-inline';font-src * data: blob: 'unsafe-inline';");
    return next();
});
app.use(express.static('./public'));
app.listen(13000, () => console.log('listening on port 13000'));

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

// api to recieve dict wit open trades
app.get('/openTrades', (request, response) => {
	// create empty dict
	var dict = {};
	// check for open trades
        const text = 'SELECT count(*) from table001 where takeprofit is not null and resultpercent is null;'
        const client = new Client({
		            user: process.env.dbUser,                                                                  host: process.env.dbHost,                                                                  database: process.env.dbName,
		            password: process.env.POSTGRES_PASSWORD,
		            port: process.env.dbPort
		        });
	client.connect();
	client
	.query(text)
	.then(res => { 
	        console.log(res.rows[0]['count'])
		response.json(res.rows[0]['count']) 
	})
	.catch(e => console.error(e.stack))
	client.end;
});

// api to recieve mean result percent
app.get('/meanResult', (request, response) => {
	// create empty dict
	var dict = {};
	// check for open trades
        const text = 'SELECT avg(resultpercent) FROM table001;'
        const client = new Client({
		            user: process.env.dbUser,                                                                  host: process.env.dbHost,                                                                  database: process.env.dbName,
		            password: process.env.POSTGRES_PASSWORD,
		            port: process.env.dbPort
		        });
	client.connect();
	client
	.query(text)
	.then(res => { 
	        console.log(res.rows[0]['avg'])
		response.json(res.rows[0]['avg']) 
	})
	.catch(e => console.error(e.stack))
	client.end;
});
