import psutil, time, sys, signal, csv

stop = False
def handler(sig, frame):
    global stop
    stop = True
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

interval = 1.0
log_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/cpu_log.csv"

with open(log_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "cpu_percent"])
    while not stop:
        cpu = psutil.cpu_percent(interval=interval)
        writer.writerow([time.time(), cpu])
