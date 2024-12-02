import os
import zipfile
import hashlib
from datetime import datetime
import json

def calculate_checksum(file_path):
    """Вычисление контрольной суммы файла (SHA-256)."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def backup_files(data_dir, backup_dir):
    os.makedirs(backup_dir, exist_ok=True)

    current_date = datetime.now().strftime("%Y%m%d")    # текущее время
    backup_name = f"backup_{current_date}.zip"          # название архива
    backup_path = os.path.join(backup_dir, backup_name)

    # Список для контрольной информации
    control_data = []

    # Создание архива
    with zipfile.ZipFile(backup_path, 'w') as backup_zip:
        for root, _, files in os.walk(data_dir):  #Рекурсивно проходит по всем подкаталогам и файлам в указанной директории data_dir.
            # Возвращает три значения:
            # root — текущая директория.
            # _ — список подкаталогов (в данном случае не используется, поэтому _).
            # files — список файлов в текущей директории.
            # Этот цикл проходит по всем директориям и их файлам.
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, start=data_dir)
                # Вычисляем контрольную сумму
                checksum = calculate_checksum(file_path)
                file_size = os.path.getsize(file_path)
                # Добавляем в контрольные данные
                control_data.append({
                    "file": relative_path,
                    "size": file_size,
                    "checksum": checksum
                })
                # Добавляем файл в архив
                backup_zip.write(file_path, relative_path)
    
        # Добавляем контрольный файл в архив
        control_file = "control.json"
        with open(control_file, 'w') as f:
            json.dump(control_data, f, indent=4)
        backup_zip.write(control_file, control_file)
        os.remove(control_file)  # Удаляем временный файл

    print(f"Резервная копия {backup_name} создана: {backup_path}")
    return backup_path

def verify_checksum(file_path, expected_checksum):
    """Проверка контрольной суммы."""
    return calculate_checksum(file_path) == expected_checksum

def restore_files(backup_path, restore_dir):
    # Восстановление архива
    os.makedirs(restore_dir, exist_ok=True)     # если каталога нет - создать
    
    with zipfile.ZipFile(backup_path, 'r') as backup_zip:
        backup_zip.extractall(restore_dir)
    
    kod = True      # собирает ошибки
    # Проверка контрольных данных, читаем контрольный файл
    control_file_path = os.path.join(restore_dir, "control.json")
    with open(control_file_path, 'r') as f:
        control_data = json.load(f)

    # Проверка файлов
    for file_info in control_data:
        relative_path = file_info["file"]
        restored_file_path = os.path.join(restore_dir, relative_path)
    
        if not os.path.exists(restored_file_path):
            print(f"Файл отсутствует: {relative_path}")
            kod = False
            continue
    
        # Проверяем размер
        if os.path.getsize(restored_file_path) != file_info["size"]:
            print(f"Размер не совпадает: {relative_path}")
            kod = False
            continue

        # Проверяем контрольную сумму
        if not verify_checksum(restored_file_path, file_info["checksum"]):
            print(f"Контрольная сумма не совпадает: {relative_path}")
            kod = False
        else:
            print(f"Файл в порядке: {relative_path}")
    return kod

# Пути
current_dir = os.getcwd()                   # текущая директория
data_dir = os.path.join(current_dir, "project_root", "data")        # директория с исходными данными
backup_dir = os.path.join(current_dir, "project_root", "backups")   # директория для бэкапа

# архивирование файлов по адресу data_dir
backup_path  = backup_files(data_dir, backup_dir)   # полное имя файла-бэкапа

# восстановление архива в директорию restore_dir
restore_dir = os.path.join(current_dir,"project_root","restored_data")

if restore_files(backup_path, restore_dir):
    print(f"Разархивирование прошло успешно.")
else:
    print(f"При восстановлении файлов из архива обнаружены ошибки.")