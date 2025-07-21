from flask import Flask, Response
from prometheus_client import start_http_server, Gauge, generate_latest
import random
import time
import threading

app = Flask(__name__)

# Create a custom gauge metric for CPU usage
cpu_usage = Gauge('app_cpu_usage_percent', 'Simulated CPU usage in percent')

# Background thread to simulate CPU usage
def generate_fake_cpu_usage():
    while True:
        usage = random.randint(85, 100)  # Simulated CPU usage > 80%
        cpu_usage.set(usage)
        print(f"[Metric Update] CPU Usage: {usage}%")
        time.sleep(10)

# Start the background thread
threading.Thread(target=generate_fake_cpu_usage, daemon=True).start()

@app.route('/')
def hello():
    return "Sample App is running..."

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

