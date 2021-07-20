async function getsimulatedSum() {
	const simulatedSumResponse = await fetch('/simulatedSum');
	const simulatedSumData = await simulatedSumResponse.json();
	document.getElementById("simulatedSum").innerHTML = simulatedSumData.data;
};

getsimulatedSum();
setInterval(getsimulatedSum, 10000);