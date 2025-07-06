from menu import main_menu
from utils import getDateTime, delete_folder, create_folder, copy_folder


# Base settings
_serverDir = r'C:\Server\tactical_life\dev_server'
_backupDir = r'C:\backup'
create_folder(r'C:\\', 'backup')


# Profile settings
_profileName = '!ATVProfile'
_profileDir = rf'{_serverDir}\{_profileName}'
_profileFilterFolders = ['Users']
_profileFilterFiles = ['config.cfg', 'basic.cfg']

#delete_folder(_profileDir, _profileFilterFolders)

#copy_folder(_serverDir, _backupDir, _profileName)

