async function getAssets() {
	const assetsResponse = await fetch('/assets');
	const assetsData = await assetsResponse.json();
	document.getElementById("amount").innerHTML = parseFloat(assetsData).toPrecision(3) + " BNB";
	setTimeout( getHistory, 5000 );
};
getAssets();
