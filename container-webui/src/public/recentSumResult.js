async function getHistory() {
	const resultResponse = await fetch('/recentSumResult');
	const resultData = await resultResponse.json();
	document.getElementById("recentSumResult").innerHTML = parseFloat(resultData).toPrecision(3) + " %";
	setTimeout( getHistory, 5000 );
};
getHistory();
