
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

openTrades = pd.DataFrame(postgres.sqlQuery(sql))
if len(openTrades) > 0:
    #initiate empty output dataframe
    for index, row in openTrades.iterrows():
        #query for simulated stopid
        sql = ("SELECT bidprice" +
            " FROM " + self.dbTable + " WHERE" +
            " symbol = '" + row[0] +
            "' ORDER BY id DESC LIMIT 1;")
        stopId = pd.DataFrame(postgres.sqlQuery(sql))
        resultPercent.append(((float(stopId[0][0]) - float(row[1])) / float(row[1])) * 100 - self.brokerFees * 2)
    r.setex(
        "simulatedAvg",
        timedelta(minutes=15),
        value=str(round(sum(resultPercent)/len(resultPercent), 2)) + " %"
    )
    if self.liveTrading:    
        r.setex(
            "simulatedSum",
            timedelta(minutes=15),
            value=str(round(sum(resultPercent)/100 * self.liveVolume, 2)) + " " + self.baseCurrency
        )
    else:
        r.setex(
            "simulatedSum",
            timedelta(minutes=15),
            value=str(round(sum(resultPercent), 2)) + " %"
        )
    r.setex(
        "simulatedWinner",
        timedelta(minutes=15),
        value=round(sum(i > 0 for i in resultPercent), 2)
    )  
    r.setex(
        "simulatedLoser",
        timedelta(minutes=15),
        value=round(sum(i < 0 for i in resultPercent), 2)
    )
else: