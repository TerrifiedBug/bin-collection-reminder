#!/bin/bash
set -e

# Setup the cron job based on environment variable or default to Monday at 6PM
CRON_SCHEDULE=${CRON_SCHEDULE:-"0 18 * * 1"}

# Create the cron job
echo "$CRON_SCHEDULE cd /app && python3 -m scripts.bin_collection >> /var/log/cron.log 2>&1" > /etc/cron.d/bincollection
chmod 0644 /etc/cron.d/bincollection

# Apply cron job
crontab /etc/cron.d/bincollection

# Create the log file to be able to see logs
touch /var/log/cron.log

# Run the script once at startup
python3 -m scripts.bin_collection

# Start cron in the foreground
cron && tail -f /var/log/cron.log
