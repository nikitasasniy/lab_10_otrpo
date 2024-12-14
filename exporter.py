from prometheus_client import Gauge, start_http_server
import psutil
import time
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Метрики с метками
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage in percent per core', ['core'])
memory_total = Gauge('memory_total_bytes', 'Total memory in bytes')
memory_used = Gauge('memory_used_bytes', 'Used memory in bytes')
disk_total = Gauge('disk_total_bytes', 'Total disk space in bytes', ['disk'])
disk_used = Gauge('disk_used_bytes', 'Used disk space in bytes', ['disk'])

# Функция обновления метрик
def update_metrics():
    # Сбор метрик процессора по каждому ядру
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cpu_usage.labels(core=f"core_{i}").set(percentage)

    # Сбор метрик памяти
    mem = psutil.virtual_memory()
    memory_total.set(mem.total)
    memory_used.set(mem.used)

    # Сбор метрик по каждому диску
    for part in psutil.disk_partitions():
        if 'cdrom' in part.opts or part.fstype == '':
            continue  # Пропускаем CD-ROM и пустые диски
        usage = psutil.disk_usage(part.mountpoint)
        disk_total.labels(disk=part.device).set(usage.total)
        disk_used.labels(disk=part.device).set(usage.used)

if __name__ == '__main__':
    # Чтение переменных окружения
    host = os.getenv('EXPORTER_HOST', '0.0.0.0')
    port = int(os.getenv('EXPORTER_PORT', '8000'))

    # Запуск HTTP-сервера
    start_http_server(port, addr=host)
    print(f"Exporter running on {host}:{port}")

    # Циклическое обновление метрик
    while True:
        update_metrics()
        time.sleep(5)
