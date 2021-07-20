async function getsimulatedLoser() {
	const simulatedLoserResponse = await fetch('/simulatedLoser');
	const simulatedLoserData = await simulatedLoserResponse.json();
	document.getElementById("simulatedLoser").innerHTML = simulatedLoserData.data;
};

getsimulatedLoser();
setInterval(getsimulatedLoser, 10000);