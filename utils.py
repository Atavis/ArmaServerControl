import subprocess
import datetime
import shutil
import os
from pathlib import Path
import stat

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
    """Архивирует каталог в ZIP-файл. """

    try:
        shutil.make_archive(os.path.splitext(_dirSave)[0], 'zip', _dir)  # Создает архив без расширения .zip
        print(f"Каталог '{_dir}' успешно заархивирован в '{_dirSave}'")
    except Exception as e:
        print(f"Ошибка при архивировании каталога: {e}")        
        
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
    extensions = [ext.lower() for ext in extensions]  # для надёжности
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            if ext.lower() in extensions:
                try:
                    os.remove(file_path)
                    print(f"Удалён файл: {file_path}")
                except Exception as e:
                    print(f"Ошибка при удалении файла {file_path}: {e}")