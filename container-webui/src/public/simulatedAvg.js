async function getsimulatedAvg() {
	const simulatedAvgResponse = await fetch('/simulatedAvg');
	const simulatedAvgData = await simulatedAvgResponse.json();
	document.getElementById("simulatedAvg").innerHTML = simulatedAvgData.data;
};

getsimulatedAvg();
setInterval(getsimulatedAvg, 10000);