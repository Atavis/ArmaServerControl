from inquirer import prompt
import inquirer


def main_menu():
    _mainList = [
        inquirer.List('main_menu',
        message = "Управление серверов",
        choices = [
            'Запустить сервер',
            'Выход'
        ])
    ]
    _choiceMainList = prompt(_mainList)['main_menu']