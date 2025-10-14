import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("vwt.csv")

df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

plt.figure(figsize=(10, 6))
plt.plot(df['Time'], df['No.'])
plt.title('Packets Captured Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Packet Number')
plt.grid(True)
plt.savefig('packets_over_time.png')
plt.show()

protocol_counts = df['Protocol'].value_counts()

plt.figure(figsize=(8,6))
protocol_counts.plot(kind='bar')
plt.title("Packets by Protocol")
plt.xlabel("Protocol")
plt.ylabel("Count")
plt.savefig('packets_by_protocol.png')
plt.show()

# Combine source and destination counts
ip_counts = df['Source'].value_counts() + df['Destination'].value_counts()
top_ips = ip_counts.sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
top_ips.plot(kind='bar')
plt.title("Top 10 Active IP Addresses")
plt.xlabel("IP Address")
plt.ylabel("Number of Packets")
plt.savefig('top_10_ips.png')
plt.show()

plt.figure(figsize=(10,5))
plt.hist(df['Length'], bins=50)
plt.title("Packet Length Distribution")
plt.xlabel("Packet Size (bytes)")
plt.ylabel("Frequency")
plt.savefig('packet_length_distribution.png')
plt.show()