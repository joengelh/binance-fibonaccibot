async function getHistory() {
	const openTradesResponse = await fetch('/openTrades');
	const openTradesData = await openTradesResponse.json();
	console.log(openTradesData);
	document.getElementById("open").innerHTML = openTradesData;
};
getHistory();
