import subprocess
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
    
def backup_mysql_database(username, password, database_name, backup_dir, mysql_path):
    """
    Создает дамп базы данных MySQL с использованием mysqldump, включая функции.

    Args:
        username: Имя пользователя MySQL.
        password: Пароль пользователя MySQL.
        database_name: Имя базы данных для резервного копирования.
        backup_dir: Каталог, в котором будут храниться резервные копии.
        mysql_path: Путь к исполняемому файлу mysqldump (mysqldump.exe) в OpenServer.
    """
    try:
        now = datetime.datetime.now()
        backup_file = os.path.join(backup_dir, f"{database_name}_{now.strftime('%Y%m%d_%H%M%S')}.sql")

        # Команда mysqldump
        command = [
            mysql_path,  # Укажите полный путь к mysqldump.exe
            "-u", username
            ]
        if password: # Добавляем пароль только если он есть
            command.append(f"-p{password}")
        command.extend([ # Добавляем остальные аргументы
            "--compact",            
            "--routines",      # Включаем дампинг хранимых процедур и функций
            database_name
        ])

        # Выполнение команды и перенаправление вывода в файл
        with open(backup_file, "w", encoding="utf-8") as outfile:  # Открываем файл для записи
            process = subprocess.Popen(command, stdout=outfile, stderr=subprocess.PIPE)
            _, stderr = process.communicate() # Получаем stdout и stderr

        if process.returncode != 0:
            print(f"Ошибка при создании резервной копии (код ошибки: {process.returncode}):")
            if stderr:
                print(f"Сообщение об ошибке:\n{stderr.decode('utf-8')}")
            raise subprocess.CalledProcessError(process.returncode, command, stderr=stderr)

        print(f"Резервная копия базы данных '{database_name}' успешно создана (включая функции): {backup_file}")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании резервной копии: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


# Пример использования:
username = "root"  # Замените на ваше имя пользователя MySQL
password = ""      # Замените на ваш пароль MySQL (или оставьте пустым для интерактивного ввода)
database_name = "tactical_life"  # Замените на имя вашей базы данных
backup_dir = r"C:\backup"  # Замените на путь к каталогу для резервных копий. Обязательно создайте эту папку.
mysql_path = r"C:\Влад\Игры\Arma 3\OpenServer\modules\database\MySQL-5.7\bin\mysqldump.exe" #  Замените на реальный путь к mysqldump.exe

backup_mysql_database(username, password, database_name, backup_dir, mysql_path)