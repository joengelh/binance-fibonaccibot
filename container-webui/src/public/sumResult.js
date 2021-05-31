async function getHistory() {
	const meanResultResponse = await fetch('/sumResult');
	const meanResultData = await meanResultResponse.json();
	console.log(meanResultData);
	document.getElementById("sum").innerHTML = meanResultData;
};
getHistory();
