async function getsimulatedWinner() {
	const simulatedWinnerResponse = await fetch('/simulatedWinner');
	const simulatedWinnerData = await simulatedWinnerResponse.json();
	document.getElementById("simulatedWinner").innerHTML = simulatedWinnerData.data;
};

getsimulatedWinner();
setInterval(getsimulatedWinner, 10000);