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

# Insert a new maintenance task into the maintenance_tasks table
def insert_maintenance_task(db, task_name, status):
    try:
        cursor = db.cursor()
        query = "INSERT INTO maintenance_tasks (task_name, status) VALUES (%s, %s)"
        cursor.execute(query, (task_name, status))
        db.commit()
        print(f"Maintenance task added: {task_name} - Status: {status}")
    except mysql.connector.Error as err:
        print(f"Error adding maintenance task: {err}")
        db.rollback()

# Update the status of an existing maintenance task
def update_task_status(db, task_id, status):
    try:
        cursor = db.cursor()
        query = "UPDATE maintenance_tasks SET status = %s WHERE id = %s"
        cursor.execute(query, (status, task_id))
        db.commit()
        print(f"Task ID {task_id} status updated to: {status}")
    except mysql.connector.Error as err:
        print(f"Error updating task status: {err}")
        db.rollback()

# Fetch all maintenance tasks from the maintenance_tasks table
def fetch_maintenance_tasks(db):
    try:
        cursor = db.cursor()
        query = "SELECT * FROM maintenance_tasks ORDER BY timestamp DESC"
        cursor.execute(query)
        results = cursor.fetchall()
        print("Fetching all maintenance tasks:")
        for task in results:
            print(task)
    except mysql.connector.Error as err:
        print(f"Error fetching maintenance tasks: {err}")

# Main script
if __name__ == "__main__":
    # Connect to the database
    db = connect_to_database()
    
    if db:
        # Example: Insert a new maintenance task
        insert_maintenance_task(db, "Disk Cleanup", "In Progress")
        
        # Example: Update the task status (assuming task ID 1)
        update_task_status(db, 1, "Completed")
        
        # Fetch all maintenance tasks
        fetch_maintenance_tasks(db)

        # Close the connection
        db.close()
        print("Database connection closed.")
