from menu import main_menu
from utils import getDateTime, delete_folder, create_folder, copy_folder, dump_mysql_db, remove_folder, remove_files_with_extensions
import shutil
import os
import configparser

config = configparser.ConfigParser()
config.read('settings.ini', encoding='utf-8')

# Base settings
_serverDir = config.get('server', 'server_dir')
_backupDir = config.get('server', 'server_backups')

# Profile settings
_profileName = config.get('profile', 'folder_name')
_profileFilterFiles = config.get('profile', 'filter_files')
_profileFilterFolders = config.get('profile', 'filter_folders')
_profileDir = rf'{_serverDir}\{_profileName}'

# extdb3

# MySQL
mysqldump_dir = config.get('mysql', 'mysqldump_dir')

def dumpFiles():
    # Создаем папки
    _mainFolder = create_folder(_backupDir, getDateTime())
    _profileFolder = create_folder(_mainFolder, 'Профиль')
    _dbFolder = create_folder(_mainFolder, 'БД')
    _extdbFolder = create_folder(_mainFolder, 'extdb3')
    
    # Профиль
    delete_folder(_profileDir, _profileFilterFolders)           # Удаляем с профиля лишние папки
    copy_folder(_serverDir, _profileFolder, _profileName)       # Копируем профиль
    
    # Копируем БД
    dump_mysql_db(
        user='root',
        host='localhost',
        db_name='tactical_life', 
        mysqldump_path=mysqldump_dir, 
        dump_dir=_dbFolder
    )

    # Создаем архив
    shutil.make_archive(
        base_name=_mainFolder,
        format='zip',
        root_dir=_backupDir,
        base_dir=os.path.basename(_mainFolder)
    )
    
    # Удаляем исходную папку
    remove_folder(_mainFolder)
    
    # Очищаем папку профиля от мусора
    remove_files_with_extensions(_profileDir, ['.log', '.rpt'])

dumpFiles()


