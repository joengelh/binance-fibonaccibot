async function getAssets() {
	const assetsResponse = await fetch('/assets');
	const assetsData = await assetsResponse.json();
	document.getElementById("amount").innerHTML = assetsData;
};

getAssets();
setInterval(getAssets, 10000);
