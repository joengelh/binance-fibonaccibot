async function getHistory() {
	const meanResultResponse = await fetch('/sumResult');
	const meanResultData = await meanResultResponse.json();
	document.getElementById("sum").innerHTML = meanResultData;
};

getHistory();
setInterval(getHistory, 10000);
