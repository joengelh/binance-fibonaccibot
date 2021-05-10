async function getHistory() {
	const meanResultResponse = await fetch('/meanResult');
	const meanResultData = await meanResultResponse.json();
	console.log(meanResultData);
	document.getElementById("mean").innerHTML = meanResultData;
};
getHistory();
