#!/bin/bash

# List of services to restart
services=("httpd" "mysql")

# Loop through each service and attempt to restart
for service in "${services[@]}"; do
    echo "Restarting $service..."
    if systemctl restart "$service"; then
        echo "$service restarted successfully."
    else
        echo "Failed to restart $service."
    fi
done
