# Set-ExecutionPolicy Unrestricted -Force

from menu import main_menu
from utils import getDateTime, delete_folder, create_folder, copy_folder, dump_mysql_db, remove_folder, remove_files_with_extensions, archive_directory, find_log_files, copy_files
import configparser
import json

# Открываем файл в режиме чтения
with open('settings.json', 'r', encoding='utf-8') as file:
    # Загружаем содержимое файла в переменную
    data = json.load(file)

# Base settings
_serverDir = data['server']['dir']
_backupDir = data['server']['dir_backups']

# Profile settings
_profileName = data['profile']['name']
_profileFilterFilesClear = data['profile']['filter_files']
_profileFilterFolders = data['profile']['filter_folders']
_profileDir = rf'{_serverDir}\{_profileName}'

# extdb3
_extdbName = data['extdb']['name']
_extdbFilterFilesSearh = data['extdb']['filter_files']
_extdbDir = rf'{_serverDir}\{_extdbName}\logs'

# MySQL
mysqldump_dir = data['mysql']['dir']

def dumpFiles():
    # Создаем папки
    _mainFolder = create_folder(_backupDir, getDateTime())
    _profileFolder = create_folder(_mainFolder, 'Profile')
    _dbFolder = create_folder(_mainFolder, 'DataBase')
    _extdbFolder = create_folder(_mainFolder, 'extdb3 logs')
    
    # Профиль
    delete_folder(_profileDir, _profileFilterFolders)           # Удаляем с профиля лишние папки
    copy_folder(_serverDir, _profileFolder, _profileName)       # Копируем профиль
    
    # extdb
    _logList = find_log_files(_extdbDir, _extdbFilterFilesSearh)
    copy_files(_logList, _extdbFolder)
    remove_folder(_extdbDir)
    
    # Копируем БД
    dump_mysql_db(
        user='root',
        host='localhost',
        db_name='tactical_life', 
        mysqldump_path=mysqldump_dir, 
        dump_dir=_dbFolder
    )

    # Создаем архив
    archive_directory(_mainFolder, _backupDir)
    
    # Удаляем исходную папку
    remove_folder(_mainFolder)
    
    # Очищаем папку профиля от мусора
    remove_files_with_extensions(_profileDir, _profileFilterFilesClear)

dumpFiles()

