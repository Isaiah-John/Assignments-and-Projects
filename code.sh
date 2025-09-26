#!/bin/bash

# This script backs up a directory to a specified destination with a timestamp.
# Usage: ./backup.sh /path/to/source /path/to/destination

# Input validation
if [ $# -ne 2 ]; then
  echo "Usage: $0 /home/test/ITMS/code.sh /home/test/448"
  exit 1
fi

SOURCE="/home/test/ITMS"
DEST="/home/test/448"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_NAME="backup_$TIMESTAMP.tar.gz"

# Create backup
echo "Creating backup of $SOURCE at $DEST/$BACKUP_NAME..."
tar -czf "$DEST/$BACKUP_NAME" "$SOURCE"

# Check if the backup was successful
if [ $? -eq 0 ]; then
  echo "Backup completed successfully: $DEST/$BACKUP_NAME"
else
  echo "Backup failed."
  exit 2
fi
