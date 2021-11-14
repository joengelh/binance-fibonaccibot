// import modules
require('dotenv').config();
const express = require('express');
const app = express();
const redis = require("redis");

// serve static index.html
app.use(function(req, res, next) {
    res.setHeader("Content-Security-Policy", "default-src *  data: blob: filesystem: about: ws: wss: 'unsafe-inline' 'unsafe-eval' 'unsafe-dynamic'; script-src * 'unsafe-inline' 'unsafe-eval'; connect-src * 'unsafe-inline'; img-src * data: blob: 'unsafe-inline'; frame-src *; style-src * data: blob: 'unsafe-inline';font-src * data: blob: 'unsafe-inline';");
    return next();
});
app.use(express.static('./public'));
app.listen(13000, () => console.log('listening on port 13000'));

// load redis connection vars from environment
const redisClient = redis.createClient({
	    host: process.env.dbHost,
	    password: process.env.POSTGRES_PASSWORD
});

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
