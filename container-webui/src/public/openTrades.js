async function getHistory() {
	const openTradesResponse = await fetch('/openTrades');
	const openTradesData = await openTradesResponse.json();
	document.getElementById("open").innerHTML = openTradesData;
        setTimeout( getHistory, 5000 );
};
getHistory();
