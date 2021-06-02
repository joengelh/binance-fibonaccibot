async function getHistory() {
	const meanResultResponse = await fetch('/sumResult');
	const meanResultData = await meanResultResponse.json();
	document.getElementById("sum").innerHTML = parseFloat(meanResultData).toPrecision(3) + " %";
};
getHistory();
