import os

def clean_logs():
    print("Cleaning log files...")
    log_dirs = ['/var/log', '/tmp']
    for directory in log_dirs:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    clean_logs()
