import os
import shutil
import psutil
from datetime import datetime, timedelta

def cleanup_old_files(directory, days=7):
    threshold_date = datetime.now() - timedelta(days=days)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_modified < threshold_date:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

def check_disk_space(threshold=90):
    disk_usage = psutil.disk_usage('/')
    usage_percent = disk_usage.percent
    print(f"Disk usage: {usage_percent}%")
    if usage_percent > threshold:
        print("Disk usage exceeded threshold. Cleaning up old files...")
        cleanup_old_files('/home/vishnuvrd/project/temp', days=7)

if __name__ == "__main__":
    check_disk_space()
