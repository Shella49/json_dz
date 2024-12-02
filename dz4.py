import os
from datetime import datetime
import datetime
import json

class FileInfo:
    def __init__(self, name, path, size, creation_date, modification_date):
        self.name = name
        self.path = path
        self.size = size
        self.creation_date = creation_date
        self.modification_date = modification_date

    def to_dict(self):
        """Преобразует объект в словарь для сериализации."""
        return {
            "name": self.name,
            "path": self.path,
            "size": self.size,
            "creation_date": self.creation_date,
            "modification_date": self.modification_date,
        }

    @classmethod
    def from_dict(cls, data):
        """Создает объект FileInfo из словаря."""
        return cls(
            name=data["name"],
            path=data["path"],
            size=data["size"],
            creation_date=data["creation_date"],
            modification_date=data["modification_date"],
        )

def get_file_info(file_path):
    """Собирает информацию о файле."""
    name = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    creation_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
    modification_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
   
    return FileInfo(
        name=name,
        path=file_path,
        size=size,
        creation_date=creation_date,
        modification_date=modification_date,
    )

def gather_files_info(directory):
    """Собирает информацию обо всех файлах в директории."""
    file_infos = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            print(f"Файл {file} ")
            file_path = os.path.join(root, file)
            file_infos.append(get_file_info(file_path))
    return file_infos

def save_to_json(file_infos, output_path):
    """Сохраняет список объектов FileInfo в JSON-файл."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump([file_info.to_dict() for file_info in file_infos], f, ensure_ascii=False, indent=4)

current_dir = os.getcwd()                   # текущая директория
data_dir = os.path.join(current_dir, "project_root", "data", "processed")  

output_path = "files_info.json"
file_infos = gather_files_info(data_dir)

save_to_json(file_infos, output_path)
print(f"Информация о файлах сохранена в {output_path}")

# Восстановление данных из JSON
def check_file_size(file_info):
    """Проверяет, соответствует ли размер файла данным в объекте FileInfo."""
    if not os.path.exists(file_info.path):
        print(f"Ошибка: файл {file_info.name} не найден.")
        return False

    current_size = os.path.getsize(file_info.path)
    if current_size != file_info.size:
        print(f"Предупреждение: Размер файла {file_info.name} отличается! (ожидался {file_info.size}, найден {current_size})")
        return False
    else:
        print(f"Размер файла {file_info.name} соответствует ожиданиям.")
        return True

def load_from_json(input_path):
    """Загружает список объектов FileInfo из JSON-файла."""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [FileInfo.from_dict(item) for item in data]

# Пример вызова
input_path = "files_info.json"
loaded_file_infos = load_from_json(input_path)
for file_info in loaded_file_infos:
        print(file_info.name, file_info.path, file_info.size)
        # Проверка размера файла после восстановления
        check_file_size(file_info)

# Создание JSON Schema
# JSON Schema
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "path": {"type": "string"},
            "size": {"type": "integer"},
            "creation_date": {"type": "string", "format": "date-time"},
            "modification_date": {"type": "string", "format": "date-time"}
        },
        "required": ["name", "path", "size", "creation_date", "modification_date"]
    }
}

# Сохранение в файл
with open("schema.json", "w", encoding="utf-8") as f:
    json.dump(schema, f, ensure_ascii=False, indent=4)

print("Схема сохранена в файл schema.json")

# Валидация JSON-файла
from jsonschema import validate, ValidationError

def validate_json(json_file, schema_file):
    """Проверяет JSON-файл на соответствие JSON Schema."""
    with open(json_file, 'r', encoding='utf-8') as jf:
        data = json.load(jf)

    with open(schema_file, 'r', encoding='utf-8') as sf:
        schema = json.load(sf)

    try:
        validate(instance=data, schema=schema)
        print("JSON файл валиден.")
    except ValidationError as e:
        print("Ошибка валидации JSON:", e)

# Пример вызова
validate_json("files_info.json", "schema.json")

