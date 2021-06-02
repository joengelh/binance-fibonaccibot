async function getHistory() {
	const resultResponse = await fetch('/recentSumResult');
	const resultData = await resultResponse.json();
	document.getElementById("recentSumResult").innerHTML = parseFloat(resultData).toPrecision(3) + " %";
};
getHistory();
