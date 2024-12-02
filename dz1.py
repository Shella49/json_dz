import os
from datetime import datetime

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_log(message:str):
    file_path = root + "\logs\log.txt"
    with open(file_path, "a") as log_file:
        log_file.write(f"[{get_current_datetime()}] {message}\n")

def print_log():
    file_path = root + "\logs\log.txt"
    with open(file_path, "r") as log_file:
        for line in log_file:
            print(line, end="")  # end="" чтобы избежать двойного переноса строк

def dir_create(name_dir:str):
      for name in name_dir:
        try:
            os.mkdir(name)
            message = f' создана директория {name}'
            write_log(message)
        except FileExistsError:
            pass
try:
    os.mkdir('project_root')  
except  FileExistsError:
    pass 
os.chdir('project_root')    # переход в каталог
root = os.getcwd()          # корневой каталог

dir_create(['logs','data','backups','output'])
dir_create(['data/raw','data/processed'])

current_dir = os.getcwd()
path = os.path.join(current_dir, "backups")
if os.path.exists(path):
    print(f'каталог {path} существует')

path = os.path.join(current_dir, "data", "raw")
if os.path.exists(path):
    print(f'каталог {path} существует')
path = os.path.join(current_dir, "data", "processed")
if os.path.exists(path):
    print(f'каталог {path} существует')
print(f'Список файлов и директорий: {os.listdir()} ')

path ='data'
print(f'Список файлов и папок в диркктории {path}: {os.listdir(path)}')
current_dir = os.getcwd()
print(f"Текущая директория: {current_dir} ")

# создание файлов
path ='data/raw/'
data1 = 'Унылая пора, очей очарованье, приятна мне твоя прощальная краса!'
data2 = 'A sad time, the charm of the eyes, your farewell beauty is pleasant to me'
data3 = "Triste temps, charme des yeux, ton adieu beauté m'est agréable"

def create_file(data, name='file.txt', encoding='utf-8'):
    with open(name, 'w', encoding=encoding) as file:
        file.write(data)
    message = f' создан файл {name}'
    write_log(message)

create_file(data1, path+'russian.txt', encoding='utf-16')
create_file(data2, path+'english.txt', encoding='Windows-1252')
create_file(data3, path+'france.txt',encoding='ISO-8859-1')

def print_log(file_path="logs/log.txt"):
    with open(file_path, "r") as log_file:
        for line in log_file:
            print(line, end="")  # end="" чтобы избежать двойного переноса строк

print_log()

