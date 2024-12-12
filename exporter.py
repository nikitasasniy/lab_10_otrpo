from prometheus_client import Gauge, start_http_server
import psutil
import time
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Метрики
cpu_usage = Gauge('cpu_usage', 'CPU usage in percent')
memory_total = Gauge('memory_total', 'Total memory in bytes')
memory_used = Gauge('memory_used', 'Used memory in bytes')
disk_total = Gauge('disk_total', 'Total disk space in bytes')
disk_used = Gauge('disk_used', 'Used disk space in bytes')

# Функция обновления метрик
def update_metrics():
    cpu_usage.set(psutil.cpu_percent(interval=1))
    mem = psutil.virtual_memory()
    memory_total.set(mem.total)
    memory_used.set(mem.used)
    disk = psutil.disk_usage('/')
    disk_total.set(disk.total)
    disk_used.set(disk.used)

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
