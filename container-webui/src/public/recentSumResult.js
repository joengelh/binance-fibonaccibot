async function getHistory() {
	const resultResponse = await fetch('/recentSumResult');
	const resultData = await resultResponse.json();
	console.log(resultData);
	document.getElementById("recentSumResult").innerHTML = resultData;
};
getHistory();
