async function getAssets() {
	const assetsResponse = await fetch('/assets');
	const assetsData = await assetsResponse.json();
	console.log(assetsData);
	document.getElementById("amount").innerHTML = assetsData + " BNB";
};
getAssets();
