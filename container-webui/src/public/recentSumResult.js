async function getHistory() {
	const resultResponse = await fetch('/recentSumResult');
	const resultData = await resultResponse.json();
	document.getElementById("recentSumResult").innerHTML = resultData.data;
};

getHistory();
setInterval(getHistory, 10000);
