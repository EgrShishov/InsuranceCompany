const oneHour = 1000 * 60 * 60;
let now = new Date().getTime();
let endTime = localStorage.getItem('endTime');

function formatTime(time) {
    const hours = Math.floor(time / (1000 * 60 * 60));
    const minutes = Math.floor(time % (1000 * 60 * 60) / (1000 * 60));
    const seconds = Math.floor((time % (1000 * 60)) / 1000);
    return `${hours < 10 ? '0' : ''}${hours}:${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}

let countdownElement = null;

export function updateCountdown() {
    now = new Date().getTime();
    const timeLeft = endTime - now;

    countdownElement = document.getElementById('counter');
    if (timeLeft > 0) {
        countdownElement.textContent = formatTime(timeLeft);
        console.log(countdownElement.textContext);
    } else {
        countdownElement.textContent = `Ka-boom`;
        localStorage.removeItem('endTime');
        clearInterval(interval);
    }
}
