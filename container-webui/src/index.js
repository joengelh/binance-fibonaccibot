// import modules
require('dotenv').config();
const { Client } = require('pg');
const express = require('express');
const yn = require('yn');
const Binance = require('node-binance-api');
const app = express();
const redis = require("redis");

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

// load redis connection vars from environment
const redisClient = redis.createClient({
	    host: process.env.dbHost,
	    password: process.env.POSTGRES_PASSWORD
});

// declare cache refresh minutes
var minutes = 1, the_interval = minutes * 60 * 1000;

// cache assets every 5 minutes
setInterval(function() {
	// cache assets
	binance.balance((error, balances) => {
		if ( error ) return console.error(error);
		redisClient.set("assets", Math.round(parseFloat(balances[process.env.baseCurrency].available)*1000)/1000 + " " + process.env.baseCurrency);
	});
		redisClient.expire("assets", 100);
}, the_interval);

// cache openTrades every 5 minutes
setInterval(function() {
	// cache openTrades
	var dict = {};
	const text = 'SELECT count(*) from ' + process.env.dbTable.toString() + ' where takeprofit is not null and resultpercent is null;'
	const client = new Client({
		user: process.env.dbUser,
		host: process.env.dbHost,
		database: process.env.dbName,
		password: process.env.POSTGRES_PASSWORD,
		port: process.env.dbPort
		});
	client.connect();
	client
	.query(text)
	.then(res => { 
		redisClient.set("openTrades", res.rows[0]['count']);
		redisClient.expire("openTrades", 100);
		client.end();
	})
	.catch(e => console.error(e.stack))
}, the_interval);

// cache sumResult
setInterval(function() {
	var dict = {};
	var text = "";
	var answer = "";
	if (yn(process.env.liveTrading)) {
		text = 'SELECT sum((resultpercent/100) * positioncost) FROM ' + 
		process.env.dbTable.toString() + ';'
		answer = process.env.baseCurrency
	} else {
		text = 'SELECT sum(resultpercent) FROM ' + 
		process.env.dbTable.toString() + ';'
		answer = "%"
	}
        const client = new Client({
		user: process.env.dbUser,
		host: process.env.dbHost,
		database: process.env.dbName,
		password: process.env.POSTGRES_PASSWORD,
		port: process.env.dbPort
		});
	client.connect();
	client
	.query(text)
	.then(res => {
		redisClient.set("sumResult", Math.round(parseFloat(res.rows[0]['sum'])*100)/100 + " " + answer);
		redisClient.expire("sumResult", 100);
	    client.end();
		})
	.catch(e => console.error(e.stack))
}, the_interval);

// cache recentSumResult
setInterval(function() {
	var dict = {};
	var recentText = "";
	var recentAnswer = "";
	if (yn(process.env.liveTrading)) {
		recentText = 'select sum((resultpercent/100) * positioncost) from ' + 
		process.env.dbTable.toString() +
		' where stopid > (select min(id) from ' + 
		process.env.dbTable.toString() +	
		' where "time" > now() - interval \'24 hours\');'
		recentAnswer = process.env.baseCurrency
	}
	else {
		recentText = 'select sum(resultpercent) from ' + 
		process.env.dbTable.toString() +
		' where "time" > now() - interval \'24 hours\';'
		recentAnswer = "%"
	}
	const client = new Client({
		user: process.env.dbUser,
		host: process.env.dbHost,
		database: process.env.dbName,
		password: process.env.POSTGRES_PASSWORD,
		port: process.env.dbPort
		});
	client.connect();
	client
	.query(recentText)
	.then(res => {
		redisClient.set("recentSumResult", Math.round(parseFloat(res.rows[0]['sum'])*100)/100 + " " + recentAnswer);
		redisClient.expire("recentSumResult", 100);
		client.end();
		})
	.catch(e => console.error(e.stack))
}, the_interval);

// get current baseCurrency balance from account
app.get('/assets', (request, response) => {
	redisClient.get('assets', (err, reply) => {
		if (err) throw err;
		response.json({ data: reply })
	});
});

// query redis for simulated average
app.get('/simulatedAvg', (request, response) => {
	redisClient.get('simulatedAvg', (err, reply) => {
		if (err) throw err;
		response.json({ data: reply })
	});
});

// query redis for simulated sum
app.get('/simulatedSum', (request, response) => {
	redisClient.get('simulatedSum', (err, reply) => {
		if (err) throw err;
		response.json({ data: reply })
	});
});

// api to recieve dict wit open trades
app.get('/openTrades', (request, response) => {
	redisClient.get('openTrades', (err, reply) => {
		if (err) throw err;
		response.json({ data: reply })
	});
});

// api to recieve sum result percent of past 24h
app.get('/recentSumResult',(request, response) => {
        redisClient.get('recentSumResult', (err, reply) => {
		if (err) throw err;
		response.json({ data: reply })
	});
});

// api to recieve sum result percent
app.get('/sumResult', (request, response) => {
        redisClient.get('sumResult', (err, reply) => {
		if (err) throw err;
		response.json({ data: reply })
	});
});

// api to recieve sum result percent
app.get('/simulatedLoser', (request, response) => {
	redisClient.get('simulatedLoser', (err, reply) => {
	if (err) throw err;
	response.json({ data: reply })
	});
});

// api to recieve sum result percent
app.get('/simulatedWinner', (request, response) => {
	redisClient.get('simulatedWinner', (err, reply) => {
	if (err) throw err;
	response.json({ data: reply })
	});
});
