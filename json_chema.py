
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