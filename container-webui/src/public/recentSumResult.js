async function getHistory() {
	const meanResultResponse = await fetch('/recentSumResult');
	const meanResultData = await meanResultResponse.json();
	console.log(meanResultData);
	document.getElementById("recentSumResult").innerHTML = meanResultData;
};
getHistory();
