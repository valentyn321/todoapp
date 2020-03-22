const startingMinutes = 25;
let time = startingMinutes * 60;

const countdownEl = document.getElementById('countdown');


function CounterCaller() {
	setInterval(updateCountDown, 1000);
}

function CounterReset() {
	const minutes = Math.floor(time / 60);
	
	let seconds = time % 60;

	seconds = seconds < 10 ? '0' + seconds : seconds

	countdownEl.innerHTML = `${minutes}:${seconds}`;
}

function updateCountDown() {
	const minutes = Math.floor(time / 60);
	
	let seconds = time % 60;

	seconds = seconds < 10 ? '0' + seconds : seconds

	countdownEl.innerHTML = `${minutes}:${seconds}`;
	
	time--;
}