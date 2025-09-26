#!/bin/bash

# This script displays system status: CPU, memory, disk, and network usage.

echo "------------- System Status Report -------------"
echo "hostname      	: $(hostname)"
echo "Date/Time   	: $(date)"
echo "Uptime        	: $(uptime -p)"
echo "------------------------------------------"


echo "CPU usage:"
top -bn1 | grep "Cpu(s)" | \
awk '{print "  User: " $2 "%, System: " $4 "%, Idle: " $8 "%"}'
echo "------------------------------------------"


echo "Mem usage:"
free -h | awk '/^Mem:/ {print "  Used: " $3 ", Free: " $4 ", Total: " $2}'
echo "------------------------------------------"


echo "Disk usage:"
df -h / | awk 'NR==2 {print "  Used: " $3 ", Free: " $4 ", Total: " $2 ", Usage: " $5}'
echo "------------------------------------------"


echo "Network Usage:"
ip -br a | awk '{print "  " $1 ": " $3}'
echo "=========================================="
