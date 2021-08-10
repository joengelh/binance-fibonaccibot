// import modules
const redis = require("redis");

// load redis connection vars from environment
const redisClient = redis.createClient({
	    host: "192.168.2.8",
	    password: "password"
});

redisClient.set('simulatedWinner', 200000);

redisClient.get('recentSumResult', (err, reply) => {
	if (err) throw err;
	console.log(reply);
});
