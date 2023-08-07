function updateBostonDate() {
    // Get the date in Boston's timezone
    const bostonTime = new Date(new Date().toLocaleString("en-US", {timeZone: "America/New_York"}));

    const month = String(bostonTime.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed in JavaScript
    const day = String(bostonTime.getDate()).padStart(2, '0');
    const year = bostonTime.getFullYear();

    // Assuming you have an element with the ID 'bostonDate' to display the date
    const dateElement = document.getElementById('date');
    if (dateElement) {
        dateElement.textContent = `${month}-${day}-${year}`;
    }
}

// Call the function once to set the initial date
updateBostonDate();

// Then update the date every minute (60000 milliseconds)
setInterval(updateBostonDate, 60000);
