async function getAssets() {
	const assetsResponse = await fetch('/assets');
	const assetsData = await assetsResponse.json();
	document.getElementById("amount").innerHTML = assetsData.data;
};

getAssets();
setInterval(getAssets, 10000);
