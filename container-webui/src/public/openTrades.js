async function getHistory() {
	const openTradesResponse = await fetch('/openTrades');
	const openTradesData = await openTradesResponse.json();
	document.getElementById("open").innerHTML = openTradesData.data;
};

getHistory();
setInterval(getHistory, 10000);
