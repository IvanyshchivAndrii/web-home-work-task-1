from collections import UserDict
import pickle
from prettytable import PrettyTable
import os


class NoteName:

    def __init__(self, name: str):
        self.__value = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name):
        self.__value = name

    def __str__(self):
        return self.__value

    def __repr__(self):
        return str(self)


class Tag:
    def __init__(self, tag=None):
        self.__value = tag

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name):
        self.__value = name

    def __str__(self):
        return self.__value

    def __repr__(self):
        return str(self)


class Note:
    def __init__(self, note):
        self.__value = note

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name: str):
        self.__value = name

    def __str__(self):
        return self.__value

    def __repr__(self):
        return str(self)


class Record:
    def __init__(self, name, tag=None, note=None):
        self.title = name
        self.tags = [] if tag is None else [tag]
        self.note = note

    def add_note(self, note: str):
        self.note = note

    def add_tag(self, tag: Tag):
        self.tags.append(tag)

    def __str__(self):
        return f'{str(self.title)}, {(str(self.tags))}, {str(self.note)}'

    def __repr__(self):
        return str(self)


class NoteBook(UserDict):

    def __init__(self, counter_index=0, *args, **kwargs):
        self.counter_index = counter_index
        super().__init__(*args, **kwargs)

    def add_record(self, record):
        self.data[record.title.value] = record


try:
    with open('NOTEBOOK.bin', 'rb') as fh:
        NOTEBOOK = pickle.load(fh)
except FileNotFoundError:
    NOTEBOOK = NoteBook()


def wrapper(funk):
    def inner(*args):
        try:
            return funk(*args)
        except ValueError as e:
            print(e)

    return inner


def add_note(*args):
    title = NoteName(input("\033[3m\033[32m{}".format('Введіть назву нотатку >>> ')))
    if title.value in NOTEBOOK.data:
        print(
            "\033[3m\033[31m{}\033[0m".format(f'Нотаток "{title.value}" вже існує. Виберыть іншу назву для нотатка!!!'))
    else:
        note = input('Введіть текст нотатку >>> ')
        tag = Tag(input('Введіть тег >>> '))

        note_rec = Record(title)
        note_rec.add_note(Note(note))

        if tag.value:
            note_rec.add_tag(tag)

        if note_rec.title.value not in NOTEBOOK.data:
            NOTEBOOK.add_record(note_rec)

        print(
            "\033[3m\033[33m{}\033[0m".format(f'Нотаток "{note_rec.title.value}" успішно додано до книги нотатків :)'))


def change_note(*args):
    title = NoteName(input("\033[3m\033[32m{}".format(f'Введіть назву нотатку, який треба змінити >>> ')))
    if title.value in NOTEBOOK.data:
        note = input('Введіть текст нотатку >>> ')
        NOTEBOOK.data[title.value].add_note(Note(note))
        print("\033[3m\033[33m{}\033[0m".format(f'Нотаток "{title.value}" успішно змінено :)'))
    else:
        print("\033[3m\033[31m{}\033[0m".format(f'Нотатка "{title}" не знайдено!!!'))


def add_tag(*args):
    title = NoteName(input("\033[3m\033[32m{}".format('Введіть назву нотатка до якого треба додати ТЕГ >>> ')))
    if title.value in NOTEBOOK.data:
        tag = Tag(input('Введіть ТЕГ >>> '))
        tag_list = [i.value for i in NOTEBOOK.data[title.value].tags]
        if tag.value not in tag_list:
            NOTEBOOK.data[title.value].add_tag(tag)
            print("\033[3m\033[33m{}\033[0m".format(f'ТЕГ "{tag.value}" успішно додано до списку тегів :)'))
        else:
            print("\033[3m\033[31m{}\033[0m".format(f'Tag "{tag.value}" вже є у списку тегів!!!'))
    else:
        print("\033[3m\033[31m{}\033[0m".format(f'Нотаток "{title}" не знайдено!!!'))


def del_note(*args):
    title = NoteName(input("\033[3m\033[32m{}".format(f'Введіть назву нотатку, який треба видалити >>> ')))
    if title.value in NOTEBOOK.data:
        note = NOTEBOOK.data.pop(title.value)
        print("\033[3m\033[33m{}\033[0m".format(f'Нотаток "{title}" успішно видалено :)'))
    else:
        print("\033[3m\033[31m{}\033[0m".format(f'Нотаток "{title}" не знайдено!!!'))


def find_note(*args):
    contact_table = PrettyTable()
    contact_table.field_names = ['Назва нотатку', 'Теги', 'Нотаток']
    title = NoteName(input("\033[3m\033[32m{}\033[0m".format('Введіть назву нотатку, який треба знайти >>> ')))
    if title.value in NOTEBOOK.data:
        tags_list = [i.value for i in NOTEBOOK.data[title.value].tags]
        contact_table.add_row([f'{title.value}',
                               ', '.join(tags_list),
                               f'{NOTEBOOK.data[title.value].note.value}'], divider=True)

        contact_table.max_width['Нотаток'] = 100
        print("\033[33m{}\033[0m".format(contact_table))
    else:
        print("\033[3m\033[33m{}\033[0m".format(f'Нотаток "{title}" не знайдено!!!'))


def find_by_tag(*args):
    contact_table = PrettyTable()
    contact_table.field_names = ['Назва нотатку', 'Теги', 'Нотаток']
    tag = Tag(input("\033[3m\033[32m{}\033[0m".format('Введіть ТЕГ для пошуку нотітків >>> ')))
    counter = 0
    for values in NOTEBOOK.data.values():
        tag_list = [i.value for i in values.tags]
        if tag.value in [i.value for i in values.tags]:
            contact_table.add_row([f'{values.title.value}',
                                   ', '.join(tag_list),
                                   f'{values.note.value}'], divider=True)
            counter += 1

    if not counter:
        print("\033[3m\033[31m{}\033[0m".format(f'Тегу {tag.value} не знайдено!!!'))

    else:
        contact_table.max_width['Нотаток'] = 100
        print(contact_table)


def show_notes(*args):
    contact_table = PrettyTable()
    contact_table.field_names = ['Назва нотатку', 'Теги', 'Нотаток']
    if not NOTEBOOK.data:
        print('В нотатнику немає нотатків!!!')
    else:
        for values in NOTEBOOK.data.values():
            tag_list = [str(i) for i in values.tags]
            contact_table.add_row([f'{values.title.value}',
                                   ', '.join(tag_list),
                                   f'{values.note.value}'], divider=True)

        contact_table.max_width['Нотаток'] = 100
        print("\033[33m{}\033[0m".format(contact_table))


def no_command(*args):
    print("Невідома команда, спробуйте ща раз!!!")


def help_table(*args):
    helper = PrettyTable()
    helper.field_names = ['Команда', 'Що виконує команда']
    helper.add_row(['add', 'додти запис в книгу нотатків'], divider=True)
    helper.add_row(['delete', 'видалити запис з книги нотатків'], divider=True)
    helper.add_row(['change', 'зиінити запис в книзі нотатків'], divider=True)
    helper.add_row(['show all', 'вивести зміст книги нотатків'], divider=True)
    helper.add_row(['find', 'знайти запис в книзі нотатків'], divider=True)
    helper.add_row(['tag', 'додати ТЕГ до запису в книзі нотатків'], divider=True)
    helper.add_row(['tg find', 'знайти записи в книзі нотатків за тегом'], divider=True)
    helper.add_row(['help', 'вивести списку команд'], divider=True)
    helper.add_row(['exit, close, good bye', 'завершити роботу з нотатником'])

    print("\033[32m{}\033[0m".format(helper))


def exit(*args):
    return "До побачння!!! Гарного Вам Дня!!!"


COMMANDS = {add_note: 'add',
            exit: ['exit', 'close', 'good bye'],
            del_note: 'delete',
            change_note: 'change',
            show_notes: 'show all',
            find_note: 'find',
            find_by_tag: 'tg find',
            add_tag: 'tag',
            help_table: 'help'
            }


def command_handler(text):
    for command, kword in COMMANDS.items():
        if isinstance(kword, str):
            if text.lower().startswith(kword):
                return command, None
        elif isinstance(kword, list):
            if text.strip().lower() in kword:
                return command, None
    return no_command, None


def clear_cli():
    match os.name:
        case 'posix':
            os.system('clear')
        case 'nt':
            os.system('cls')


def run():
    if os.name == 'nt':
        os.system('cls')
    print("\033[1m\033[36m{}".format('Привіт!!! Це ваш особистий нотатник!!!'))
    print("\033[1m\033[31m{}\033[0m".format(
        'Якщо ви увійшли в перший раз, введіть "help" та натисніть Enter для ознайомдення з можливостями нотатника :)'))
    flag = True
    while flag:
        user_input = input('>>>')
        command, data = command_handler(user_input)

        command(data)

        if command == exit:
            print(exit())
            flag = False

    with open('NOTEBOOK.bin', 'wb') as fh:
        pickle.dump(NOTEBOOK, fh)


if __name__ == '__main__':
    run()
