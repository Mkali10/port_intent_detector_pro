const socket = io();
const tableBody = document.querySelector("#connections-table tbody");
const alertsDiv = document.getElementById("alerts");
let chartData = {};

socket.on("new_connection", function(data) {
    // Add row to table
    const row = document.createElement("tr");
    if(data.suspicious){
        row.classList.add("suspicious");
        alertsDiv.innerText = "Suspicious connection detected!";
    }
    row.innerHTML = `
        <td>${data.pid}</td>
        <td>${data.name}</td>
        <td>${data.local}</td>
        <td>${data.remote}</td>
        <td>${data.proto.toUpperCase()}</td>
        <td>${data.intent}</td>
        <td>${data.suspicious ? 'Yes' : 'No'}</td>
    `;
    tableBody.prepend(row);

    // Update chart
    chartData[data.intent] = chartData[data.intent] ? chartData[data.intent]+1 : 1;
    const chartDiv = document.getElementById("chart");
    Plotly.newPlot(chartDiv, [{
        x: Object.keys(chartData),
        y: Object.values(chartData),
        type: 'bar',
        marker: {color: '#00ccff'}
    }], {
        title: 'Connection Intents Count',
        paper_bgcolor: '#1e1e2f',
        plot_bgcolor: '#1e1e2f',
        font: {color: '#fff'}
    });
});
