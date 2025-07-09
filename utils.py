import subprocess
import datetime
import shutil
import os
from pathlib import Path
import hashlib

def create_folder(parent_dir, folder_name):
    folder_path = os.path.join(parent_dir, folder_name)
    
    os.makedirs(folder_path, exist_ok=True)
    
    cmd = ['icacls', folder_path, '/grant', 'Все:(OI)(CI)F', '/T']
    
    # Указываем encoding='cp866' для корректного чтения вывода в русской консоли Windows
    subprocess.run(cmd, capture_output=True, text=True, encoding='cp866')
    
    return folder_path

def remove_folder(path):
    cmd = ['rmdir', '/S', '/Q', path]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        print(f"Папка {path} успешно удалена")
    else:
        print(f"Ошибка при удалении папки: {result.stderr}")

def getDateTime():
    _timeNow = datetime.datetime.now()
    return _timeNow.strftime("%d.%m.%Y %H-%M-%S")

def delete_folder(_dir, _filterFolders):
    """Удаляет все папки в каталоге, кроме тех, что находятся в списке исключений. """

    for item in os.listdir(_dir):
        item_path = os.path.join(_dir, item)

        if os.path.isdir(item_path) and item not in _filterFolders:
            try:
                shutil.rmtree(item_path)
                print(f"Удалена папка: {item_path}")
            except OSError as e:
                print(f"Ошибка при удалении {item_path}: {e}")

def archive_directory(_dir, _dirSave):
    shutil.make_archive(
        base_name=_dir,
        format='zip',
        root_dir=_dirSave,
        base_dir=os.path.basename(_dir)
    )
        
def copy_folder(_sourceDir, _saveDir, _saveFolder):
    """ Копирует папку !ATVProfile в новое место."""
    source_folder = os.path.join(_sourceDir, _saveFolder)
    destination_folder = os.path.join(_saveDir, _saveFolder)

    shutil.copytree(source_folder, destination_folder)
    print(f"Папка '{source_folder}' успешно скопирована в '{destination_folder}'")
    
def dump_mysql_db(user, host, db_name, mysqldump_path, dump_dir):
    if not os.path.exists(mysqldump_path):
        raise FileNotFoundError(f"mysqldump не найден по пути {mysqldump_path}")

    os.makedirs(dump_dir, exist_ok=True)
    output_file = os.path.join(dump_dir, f"{db_name}.sql")

    command = [
        mysqldump_path,
        f'-u{user}',
        f'-h{host}',
        '--routines',
        '--single-transaction',
        db_name
    ]

    with open(output_file, 'w', encoding='utf-8') as f:
        result = subprocess.run(command, stdout=f, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"Дамп базы '{db_name}' успешно сохранён в '{output_file}'")
    else:
        print(f"Ошибка при создании дампа:\n{result.stderr}")
          
def remove_files_with_extensions(folder_path, extensions):
    extensions = [ext.lower() for ext in extensions]
    print(f"Путь: {folder_path}")
    print(f"Расширения для удаления: {extensions}")
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            print(f"Обрабатываем файл: {filename}")
            _, ext = os.path.splitext(filename)
            if ext.lower() in extensions:
                try:
                    os.remove(file_path)
                    print(f"Удалён файл: {file_path}")
                except Exception as e:
                    print(f"Ошибка при удалении {file_path}: {e}")
                    
def steamid_to_md5(steam_id_str):
    # Конвертируем строку SteamID в число
    steam_id = int(steam_id_str)
    
    # Создаем объект для хранения байтов
    byte_array = b'BE'  # Префикс 'BE'
    
    # Обрабатываем младшие байты SteamID
    for _ in range(8):
        byte = steam_id & 0xFF
        byte_array += bytes([byte])
        steam_id >>= 8
    
    # Вычисляем MD5-хеш
    md5_hash = hashlib.md5(byte_array).hexdigest()
    return md5_hash

def find_log_files(_dir, _extensions):
    matched_files = []
    for dirpath, dirnames, filenames in os.walk(_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in _extensions):
                full_path = os.path.join(dirpath, filename)
                matched_files.append(full_path)
    return matched_files

def copy_files(_filesList, _dirSave):
    if not os.path.exists(_dirSave):
        os.makedirs(_dirSave)
    for file_path in _filesList:
        if os.path.isfile(file_path):
            filename = os.path.basename(file_path)
            destination = os.path.join(_dirSave, filename)
            shutil.copy2(file_path, destination)
            print(f"Скопирован {file_path} в {destination}")
        else:
            print(f"Файл не найден: {file_path}")