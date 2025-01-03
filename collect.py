import psutil
import json
import os
from datetime import datetime
import subprocess

# File path for storing metrics
METRICS_FILE = "/home/vishnuvrd/project/metrics_data.json"
REMEDIATION_SCRIPT = "/home/vishnuvrd/project/scripts/restart_services.sh"

# Thresholds
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80

def collect_metrics():
    """Collect system metrics."""
    metrics = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    return metrics

def write_metrics(metrics):
    """Write metrics to the JSON file."""
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(metrics)
    
    with open(METRICS_FILE, "w") as f:
        json.dump(data[-100:], f, indent=4)  # Keep the latest 100 entries to avoid file bloat

def trigger_remediation(metrics):
    """Trigger remediation actions if thresholds are exceeded."""
    issues_detected = False

    if metrics["cpu_usage"] > CPU_THRESHOLD:
        print(f"High CPU usage detected: {metrics['cpu_usage']}%. Triggering remediation...")
        issues_detected = True

    if metrics["memory_usage"] > MEMORY_THRESHOLD:
        print(f"High memory usage detected: {metrics['memory_usage']}%. Triggering remediation...")
        issues_detected = True

    if metrics["disk_usage"] > DISK_THRESHOLD:
        print(f"High disk usage detected: {metrics['disk_usage']}%. Triggering remediation...")
        issues_detected = True

    if issues_detected:
        result = subprocess.run(["bash", REMEDIATION_SCRIPT], capture_output=True, text=True)
        print("Remediation output:")
        print(result.stdout)
        if result.returncode != 0:
            print("Error in remediation script:")
            print(result.stderr)

def main():
    metrics = collect_metrics()
    write_metrics(metrics)
    trigger_remediation(metrics)
    print(f"Metrics collected and remediation checked at {metrics['timestamp']}.")

if __name__ == "__main__":
    main()
