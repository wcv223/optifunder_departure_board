document.addEventListener('DOMContentLoaded', function() {
    function fetchAndUpdatePredictions() {
        fetch('api/predictions/')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }
                const predictions = data.predictions;
                const tableBody = document.querySelector('#predictions-body');
                tableBody.innerHTML = '';  // clear previous rows

                predictions.forEach(prediction => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>MBTA</td>
                        <td>${prediction.departure_time}</td>
                        <td>${prediction.headsign}</td>
                        <td>${prediction.name}</td>
                        <td>${prediction.platform_code}</td>
                        <td>${prediction.status}</td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error fetching predictions:', error));
    }

    setInterval(fetchAndUpdatePredictions, 60000);  // Update every minute
});