async function getAssets() {
	const assetsResponse = await fetch('/assets');
	const assetsData = await assetsResponse.json();
	document.getElementById("amount").innerHTML = parseFloat(assetsData).toPrecision(3) + " BNB";
};

getAssets();
setInterval(getAssets, 5000);
