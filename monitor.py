from datetime import datetime
import smtplib
import psutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine, Column, Integer, Float, BigInteger, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

# Define the SystemMetrics class
class SystemMetrics(Base):
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, default=datetime.now)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    bytes_sent = Column(BigInteger)
    bytes_recv = Column(BigInteger)

# Database connection
DATABASE_URL = "mysql+pymysql://root:Vishnu%404926@localhost/server_monitoring"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Function to insert metrics into the database
def insert_metrics(cpu, memory, disk, sent, recv):
    # Get the current timestamp using Python's datetime module
    timestamp = datetime.now()
    
    # Create a new SystemMetrics object with the timestamp and other system data
    metric = SystemMetrics(
        timestamp=timestamp,  # Pass the generated timestamp here
        cpu_usage=cpu,
        memory_usage=memory,
        disk_usage=disk,
        bytes_sent=sent,
        bytes_recv=recv
    )

    try:
        # Add the metric to the session and commit it to the database
        session.add(metric)
        session.commit()
    except SQLAlchemyError as e:
        # In case of an error, rollback the transaction and print the error
        print(f"Error inserting data: {e}")
        session.rollback()
# Function to send email alerts
def send_email_alert(subject, message):
    # Email configuration
    sender_email = "projectv.vmware@gmail.com"  # Replace with your email
    sender_password = "dhqncahzjuqttvdd"    # Replace with your app-specific password
    recipient_email = "projectv.vmware@gmail.com"  # Replace with recipient's email

    try:
        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message body
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the email server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to collect system metrics
def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters()
    sent = net.bytes_sent
    recv = net.bytes_recv
    return cpu, memory, disk, sent, recv

# Main function to run the monitoring script
def main():
    cpu, memory, disk, sent, recv = get_system_stats()
    print(f"CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%, Sent: {sent}, Received: {recv}")
    insert_metrics(cpu, memory, disk, sent, recv)
    print(f"Metrics stored: CPU {cpu}%, Memory {memory}%, Disk {disk}%")

    # Check thresholds and send alerts
    if cpu > 80:  # Example threshold for CPU usage
        send_email_alert(
            "High CPU Usage Alert",
            f"CPU usage is at {cpu}%, exceeding the 80% threshold."
        )
    if memory > 80:  # Example threshold for memory usage
        send_email_alert(
            "High Memory Usage Alert",
            f"Memory usage is at {memory}%, exceeding the 80% threshold."
        )
    if disk > 80:  # Example threshold for disk usage
        send_email_alert(
            "High Disk Usage Alert",
            f"Disk usage is at {disk}%, exceeding the 80% threshold."
        )


if __name__ == "__main__":
    main()
