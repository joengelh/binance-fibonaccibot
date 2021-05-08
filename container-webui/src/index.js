const express = require('express');
const app = express();

app.listen(13000, () => console.log('listening on port 13000'));
app.use(express.static('public'));

const Binance = require('node-binance-api');
const binance = new Binance().options({
	  APIKEY: process.env.apiKey,
	  APISECRET: process.env.apiSecret
});
binance.balance((error, balances) => {
	  if ( error ) return console.error(error);
	  console.info("BNB balance: ", balances.ETH.available);
});
