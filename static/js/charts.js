// Initialize global variables for storing chart data
let cpuData = { labels: [], values: [] };
let memoryData = { labels: [], values: [] };
let diskData = { labels: [], values: [] };

// Function to update the chart data
function updateCharts() {
    // Create or update the CPU usage chart
    const cpuCtx = document.getElementById('cpuChart').getContext('2d');
    const cpuChart = new Chart(cpuCtx, {
        type: 'line',
        data: {
            labels: cpuData.labels,  // Array of labels (time intervals)
            datasets: [{
                label: 'CPU Usage',
                data: cpuData.values,  // Array of CPU usage values
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                fill: false
            }]
        }
    });

    // Create or update the Memory usage chart
    const memoryCtx = document.getElementById('memoryChart').getContext('2d');
    const memoryChart = new Chart(memoryCtx, {
        type: 'line',
        data: {
            labels: memoryData.labels,  // Array of labels
            datasets: [{
                label: 'Memory Usage',
                data: memoryData.values,  // Array of memory usage values
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                fill: false
            }]
        }
    });

    // Create or update the Disk usage chart
    const diskCtx = document.getElementById('diskChart').getContext('2d');
    const diskChart = new Chart(diskCtx, {
        type: 'line',
        data: {
            labels: diskData.labels,  // Array of labels
            datasets: [{
                label: 'Disk Usage',
                data: diskData.values,  // Array of disk usage values
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        }
    });
}

// Function to fetch real-time system metrics from Flask API
function fetchSystemMetrics() {
    fetch('/get_system_metrics')
        .then(response => response.json())
        .then(data => {
            const timestamp = new Date().toLocaleTimeString();  // Get current time as a label
            
            // Update CPU data
            cpuData.labels.push(timestamp);
            cpuData.values.push(data.cpu_usage);
            if (cpuData.labels.length > 10) {
                cpuData.labels.shift();
                cpuData.values.shift();
            }

            // Update Memory data
            memoryData.labels.push(timestamp);
            memoryData.values.push(data.memory_usage);
            if (memoryData.labels.length > 10) {
                memoryData.labels.shift();
                memoryData.values.shift();
            }

            // Update Disk data
            diskData.labels.push(timestamp);
            diskData.values.push(data.disk_usage);
            if (diskData.labels.length > 10) {
                diskData.labels.shift();
                diskData.values.shift();
            }

            // Update the charts
            updateCharts();
        })
        .catch(error => {
            console.error('Error fetching system metrics:', error);
        });
}

// Update the charts every 2 seconds (2000ms)
setInterval(fetchSystemMetrics, 2000);
