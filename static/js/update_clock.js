function updateClock() {
    var currentTime = new Date();
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();

    minutes = (minutes < 10 ? "0" : "") + minutes;

    var timeString = hours + ':' + minutes;

    document.getElementById('clock').innerHTML = timeString;
}

setInterval(updateClock, 5000);
