import time
import random

def simulate_load():
  # Simulate CPU load by performing expensive calculations
  for _ in range(100000):
    result = sum([random.random() for _ in range(100)])

  # Simulate memory load by allocating a large array
  data = [random.random() for _ in range(100000)]
  del data  # Release memory after use

while True:
  simulate_load()
  time.sleep(1)  # Adjust sleep time to control load intensity

# Monitor system resources within the script (optional)
# You can use libraries like psutil to monitor CPU, memory usage etc.
# print(psutil.cpu_percent())
# print(psutil.virtual_memory().used / (1024 * 1024 * 1024))  # Memory usage in GB
