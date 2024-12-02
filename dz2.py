import chardet
import os
from datetime import datetime
import json

def read_all(path_in, path_out, json_dic):
    list_file = os.listdir(path_in)
    
    for name in list_file:
        path_name =os.path.join(path_in, name)
        if os.path.isfile(path_name):    # найден файл
            print(f'Найден файл {name}')
            file_dict = {}
            file_dict['file_name'] = name
            with open(path_name,'rb') as file:
                raw_data =file.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                print(f"Detected encoding: {encoding}")
                text = raw_data.decode(encoding)
                file_dict['text'] = text
                print(text)
                converted_text = text.swapcase()
                file_dict['converted_text'] = converted_text
                print(converted_text)
                # Разделяем имя и расширение
                name, extension = name.rsplit(".", 1)
                # Добавляем суффикс и собираем новое имя
                new_filename = f"{name}_processed.{extension}"
                print(new_filename)
                name_processed = os.path.join(path_out, new_filename)
                with open(name_processed,'w', encoding=encoding) as file_pr:
                    file_pr.write(converted_text)
                    # Получаем информацию о файле
                    file_dict['file_size'] = os.path.getsize(name_processed)  # Размер файла в байтах
                    last_modified_time = os.path.getmtime(name_processed)  # Время последнего изменения (в секундах с эпохи)
                    last_modified_date = datetime.fromtimestamp(last_modified_time).strftime("%Y-%m-%d %H:%M:%S")
                    file_dict['last_modified'] = last_modified_date
                     # Добавляем словарь в список
                    json_dic.append(file_dict)
json_dic = []
current_dir = os.getcwd()
path_in = os.path.join(current_dir, "project_root", "data", "raw")
path_out = os.path.join(current_dir, "project_root", "data", "processed")   
read_all(path_in, path_out, json_dic)

json_path = os.path.join(current_dir,"project_root", "output", "processed_data.json")
with open(json_path, 'w') as file:
    json.dump(json_dic, file)
