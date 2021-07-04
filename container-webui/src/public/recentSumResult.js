async function getHistory() {
	const resultResponse = await fetch('/recentSumResult');
	const resultData = await resultResponse.json();
	document.getElementById("recentSumResult").innerHTML = resultData;
};

getHistory();
setInterval(getHistory, 10000);
