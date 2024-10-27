import os
import subprocess
import paramiko

# Укажите имя пользователя и пароль
username = "your_username"
password = "your_password"

# Укажите файлы для сохранения результатов
good_file = "ssh_good.txt"
bad_file = "ssh_bad.txt"

# Удаляем старые файлы, если они существуют
if os.path.exists(good_file):
    os.remove(good_file)
if os.path.exists(bad_file):
    os.remove(bad_file)

# Функция для преобразования IP-адреса в числовой формат
def ip_to_int(ip):
    return sum(int(part) << (8 * (3 - idx)) for idx, part in enumerate(ip.split('.')))

# Функция для преобразования числового формата обратно в IP-адрес
def int_to_ip(num):
    return '.'.join(str((num >> (8 * (3 - i))) & 0xFF) for i in range(4))

# Чтение диапазонов IP из файла ip.txt
with open("ip.txt", "r") as file:
    for line in file:
        range_str = line.strip()
        start_ip, end_ip = range_str.split('-')
        start = ip_to_int(start_ip)
        end = ip_to_int(end_ip)

        # Перебор IP-адресов в диапазоне
        for i in range(start, end + 1):
            ip = int_to_ip(i)

            # Проверка доступности IP-адреса с помощью ping
            if subprocess.call(["ping", "-n", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                print(f"{ip} is not reachable, skipping...")
                continue

            print(f"Trying to connect to {ip}...")

            # Попытка подключения по SSH с использованием имени пользователя и пароля
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ip, username=username, password=password, timeout=5)
                print(f"Connection successful to {ip}!")
                with open(good_file, "a") as gf:
                    gf.write(f"{ip}\n")
                client.close()
            except Exception as e:
                print(f"Connection failed to {ip}: {e}")
                with open(bad_file, "a") as bf:
                    bf.write(f"{ip}\n")
