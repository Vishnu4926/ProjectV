import mysql.connector

# Database connection details
def connect_to_database():
    try:
        db = mysql.connector.connect(
            host="localhost",          # Change this to your database host
            user="root",      # Replace with your database username
            password="Vishnu@4926",  # Replace with your database password
            database="server_monitoring"   # Replace with your database name
        )
        print("Database connected successfully!")
        return db
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Insert an alert into the alerts table
def insert_alert(db, alert_type, message):
    try:
        cursor = db.cursor()
        query = "INSERT INTO alerts (alert_type, message) VALUES (%s, %s)"
        cursor.execute(query, (alert_type, message))
        db.commit()
        print(f"Alert added: {alert_type} - {message}")
    except mysql.connector.Error as err:
        print(f"Error adding alert: {err}")
        db.rollback()

# Fetch the most recent system metrics from the system_metrics table
def fetch_system_metrics(db):
    try:
        cursor = db.cursor()
        query = "SELECT * FROM system_metrics ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            timestamp, cpu_usage, memory_usage, disk_usage = result[1], result[2], result[3], result[4]
            print(f"Timestamp: {timestamp}, CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%, Disk Usage: {disk_usage}%")
            return cpu_usage, memory_usage, disk_usage
        else:
            print("No system metrics found.")
            return None, None, None
    except mysql.connector.Error as err:
        print(f"Error fetching system metrics: {err}")
        return None, None, None

# Check if any metric exceeds the threshold and insert an alert if necessary
def check_and_alert(db, cpu_usage, memory_usage, disk_usage, threshold=80):
    alert_triggered = False
    
    # Check CPU usage
    if cpu_usage > threshold:
        insert_alert(db, "CPU", f"CPU usage exceeded {threshold}% ({cpu_usage}% detected)")
        alert_triggered = True
    
    # Check Memory usage
    if memory_usage > threshold:
        insert_alert(db, "Memory", f"Memory usage exceeded {threshold}% ({memory_usage}% detected)")
        alert_triggered = True
    
    # Check Disk usage
    if disk_usage > threshold:
        insert_alert(db, "Disk", f"Disk usage exceeded {threshold}% ({disk_usage}% detected)")
        alert_triggered = True
    
    return alert_triggered

# Fetch all alerts from the alerts table
def fetch_alerts(db):
    try:
        cursor = db.cursor()
        query = "SELECT * FROM alerts ORDER BY timestamp DESC"
        cursor.execute(query)
        results = cursor.fetchall()
        print("Fetching all alerts:")
        for alert in results:
            print(alert)
    except mysql.connector.Error as err:
        print(f"Error fetching alerts: {err}")

# Main script
if __name__ == "__main__":
    # Connect to the database
    db = connect_to_database()
    
    if db:
        # Fetch system metrics (CPU, memory, disk usage)
        cpu_usage, memory_usage, disk_usage = fetch_system_metrics(db)
        
        # If metrics are available, check if they exceed thresholds and insert alerts
        if cpu_usage is not None and memory_usage is not None and disk_usage is not None:
            alert_triggered = check_and_alert(db, cpu_usage, memory_usage, disk_usage)

            # If alerts were triggered, fetch and display the alerts
            if alert_triggered:
                fetch_alerts(db)
        
        # Close the connection
        db.close()
        print("Database connection closed.")
