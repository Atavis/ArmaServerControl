import datetime
import shutil
import os
from pathlib import Path

def create_folder(parent_dir, folder_name):
    """
    Создаёт папку с именем folder_name в директории parent_dir.
    Если папка уже существует, ничего не делает.
    Возвращает объект Path с полным путём к папке.
    """
    parent_path = Path(parent_dir)
    folder_path = parent_path / folder_name
    if not folder_path.exists():
        folder_path.mkdir(parents=True)
        print(f"Папка '{folder_name}' создана по пути {folder_path}")
    else:
        print(f"Папка '{folder_name}' уже существует по пути {folder_path}")
    return folder_path

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