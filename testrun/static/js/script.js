// let addr = document.getElementById("player");
let download = document.getElementById("download");
let count = document.getElementById("count");
let temperature = document.getElementById("temperature");
let outputContainer = document.getElementById("output-container");
let countSpan = document.getElementById("countVal");
let tempSpan = document.getElementById("tempVal");
let style = document.getElementById("style");

// let artist = document.getElementById("artist");

// console.log(addr);
let changeShowCount = function () {
	let countVal = count.value;
	countSpan.innerHTML = countVal;
};

let changeShowTemp = function () {
	let tempVal = temperature.value;
	tempSpan.innerHTML = tempVal;
};

const midiPitchValues = {
	C0: 12,
	"C#0/Db0": 13,
	D0: 14,
	"D#0/Eb0": 15,
	E0: 16,
	F0: 17,
	"F#0/Gb0": 18,
	G0: 19,
	"G#0/Ab0": 20,
	A0: 21,
	"A#0/Bb0": 22,
	B0: 23,
	C1: 24,
	"C#1/Db1": 25,
	D1: 26,
	"D#1/Eb1": 27,
	E1: 28,
	F1: 29,
	"F#1/Gb1": 30,
	G1: 31,
	"G#1/Ab1": 32,
	A1: 33,
	"A#1/Bb1": 34,
	B1: 35,
	C2: 36,
	"C#2/Db2": 37,
	D2: 38,
	"D#2/Eb2": 39,
	E2: 40,
	F2: 41,
	"F#2/Gb2": 42,
	G2: 43,
	"G#2/Ab2": 44,
	A2: 45,
	"A#2/Bb2": 46,
	B2: 47,
	C3: 48,
	"C#3/Db3": 49,
	D3: 50,
	"D#3/Eb3": 51,
	E3: 52,
	F3: 53,
	"F#3/Gb3": 54,
	G3: 55,
	"G#3/Ab3": 56,
	A3: 57,
	"A#3/Bb3": 58,
	B3: 59,
	C4: 60,
	"C#4/Db4": 61,
	D4: 62,
	"D#4/Eb4": 63,
	E4: 64,
	F4: 65,
	"F#4/Gb4": 66,
	G4: 67,
	"G#4/Ab4": 68,
	A4: 69,
	"A#4/Bb4": 70,
	B4: 71,
	C5: 72,
	"C#5/Db5": 73,
	D5: 74,
	"D#5/Eb5": 75,
	E5: 76,
	F5: 77,
	"F#5/Gb5": 78,
	G5: 79,
	"G#5/Ab5": 80,
	A5: 81,
	"A#5/Bb5": 82,
	B5: 83,
	C6: 84,
	"C#6/Db6": 85,
	D6: 86,
	"D#6/Eb6": 87,
	E6: 88,
	F6: 89,
	"F#6/Gb6": 90,
	G6: 91,
	"G#6/Ab6": 92,
	A6: 93,
	"A#6/Bb6": 94,
	B6: 95,
	C7: 96,
	"C#7/Db7": 97,
	D7: 98,
	"D#7/Eb7": 99,
	E7: 100,
	F7: 101,
	"F#7/Gb7": 102,
	G7: 103,
	"G#7/Ab7": 104,
	A7: 105,
	"A#7/Bb7": 106,
	B7: 107,
	_: "_",
};

function mapString(inputString, characterMap) {
	// Convert the input string to an array of characters
	// console.log("input: ", inputString);
	const inputArray = inputString.split(" ");
	// console.log("Array: ", inputArray);

	// Map each character using the provided characterMap
	const mappedArray = inputArray.map((char) => {
		// console.log("char: ", char);
		// console.log(characterMap[char.trim()]);
		return characterMap[char];
	});

	// Join the mapped array back into a string
	const mappedString = mappedArray.join(" ");
	// console.log("mapped: ", mappedString);

	return mappedString;
}

function appendToTextarea(value) {
	var textarea = document.getElementById("selectedNotes");
	// var textareaHidden = document.getElementById("hiddenNotes");
	textarea.value += value + " ";
	// textareaHidden.value += value + " ";
	// textareaHidden.value = mapString(textarea.value, midiPitchValues);
	// console.log(textarea.value);
	// console.log(textareaHidden.value);
}

document.addEventListener("DOMContentLoaded", function () {
	// Example seed buttons
	const exampleSeeds = document.querySelectorAll(".example-seed");

	// Add click event listeners to example seed buttons
	exampleSeeds.forEach(function (seedButton) {
		seedButton.addEventListener("click", function () {
			const seed = seedButton.dataset.seed;
			document.getElementById("selectedNotes").value = seed;
			// document.getElementById("hiddenNotes").value = mapString(
			// 	seed,
			// 	midiPitchValues
			// );
		});
	});

	// Generate melody button
	const generateButton = document.getElementById("generate-button");

	const isSeedCheck = document.getElementById("selectedNotes");
	// const isSeedCheckValue = isSeedCheck?.value;
	generateButton.addEventListener("click", async function () {
		// console.log(isSeedCheck);/
		if (isSeedCheck) {
			seedCheck = isSeedCheck.value;
			if (seedCheck.trim() === "") {
				alert("Please enter a seed melody.");
				return;
			}
		}
		// Check if the seed is empty

		outputContainer.innerHTML = "";
		generateButton.innerHTML = "Generating...";

		generateButton.setAttribute("disabled", "");
		generateButton.style.cursor = "not-allowed";

		let radioVal = document.querySelector('input[name="length"]:checked').value;
		if (isSeedCheck) {
			let seed = document.getElementById("selectedNotes").value;
		}

		// let textareaHiddenVal = document?.getElementById("hiddenNotes");
		if (isSeedCheck) {
			document.getElementById("hiddenNotes").value = mapString(
				document.getElementById("selectedNotes").value,
				midiPitchValues
			);
		}
		// Send the seed to the server to generate the melody
		try {
			// let fin;
			// let blogs;
			console.log("sent");
			console.log(count.value);
			let sendObj = {
				// seed: seed,
				no: count.value,
				temp: temperature.value,
				genre: style.value,
				length: radioVal,
				// composer: artist.value,
			};

			if (isSeedCheck) {
				sendObj = {
					...sendObj,
					seed: document.getElementById("hiddenNotes").value,
				};
			}

			console.log(sendObj);

			const response = await fetch("http://127.0.0.1:8000/playground/hello/", {
				method: "POST",
				// mode: "no-cors",

				body: JSON.stringify(sendObj),
				headers: {
					"Content-Type": "application/json",
				},
			});

			blogs = await response.json();
			blogs = await JSON.parse(blogs);
			patharr = Object.keys(blogs);

			for (i = 0; i < patharr.length; i++) {
				// elm = document.createElement("midi-player");
				elm = document.createElement("audio");
				elm.setAttribute("controls", "");
				elm.setAttribute("src", blogs[patharr[i]]);
				// console.log("element: ", elm);
				dow = document.createElement("a");
				dow.setAttribute("href", blogs[patharr[i]]);
				dow.setAttribute("download", "");
				const downPrompt = document.createTextNode("Download");
				dow.appendChild(downPrompt);
				// console.log("element: ", dow);
				divC = document.createElement("div");
				divC.setAttribute("class", "output-containers");

				divC.appendChild(elm);
				divC.appendChild(dow);

				console.log("divC: ", divC);
				outputContainer.appendChild(divC);
				// outputContainer.appendChild(dow)
			}
			console.log("blob: ", blogs);

			generateButton.removeAttribute("disabled");
			generateButton.style.cursor = "pointer";
			generateButton.innerHTML = "Generate";
		} catch (error) {
			generateButton.removeAttribute("disabled");
			generateButton.style.cursor = "pointer";
			generateButton.innerHTML = "Generate";
			console.error("Error:", error);
		}

		// .then((response) => response.blob())
		// .then((data) => {
		// 	// const melodyOutput = document.getElementById("melody-output");
		// 	// melodyOutput.textContent = data.melody;

		// 	// // Display the download link
		// 	// const downloadLink = document.getElementById("download-link");
		// 	// downloadLink.href = "data:audio/midi;base64," + data.melodyData;
		// 	// downloadLink.style.display = "block";
		// 	console.log(response, data);
		// })
		// .catch((error) => {
		// 	console.error("Error:", error);
		// });
	});
});
