PromQL Запросы
## 1. Использование процессоров

### Среднее использование всех процессоров (в процентах):

avg(cpu_usage_percent)

### Использование каждого ядра процессора отдельно:

cpu_usage_percent

## 2. Память: всего и используется

### Процент используемой памяти:

memory_used_bytes / memory_total_bytes * 100

### Общий объем памяти:

memory_total_bytes

### Объем используемой памяти:

memory_used_bytes

## 3. Диски: общий объем и используется
### Процент использования всех дисков:
sum(disk_used_bytes) / sum(disk_total_bytes) * 100

### Процент использования каждого диска:

disk_used_bytes / disk_total_bytes * 100

### Общий объем всех дисков:

sum(disk_total_bytes)

### Общий объем используемого пространства на всех дисках:

sum(disk_used_bytes)

### Общий объем свободного пространства на всех дисках:

sum(disk_total_bytes - disk_used_bytes)