function updateClock() {
    var now = new Date();
    // Use the Intl.DateTimeFormat object to handle the conversion to Boston time
    var options = { timeZone: "America/New_York", hour: '2-digit', minute:'2-digit', second:'2-digit' };
    var formatter = new Intl.DateTimeFormat([], options);
    var time = formatter.format(now);
    document.getElementById('clock').innerHTML = time;
    setTimeout(updateClock, 1000);
}

updateClock();