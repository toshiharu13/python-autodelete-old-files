#!/usr/bin/env python3

import datetime
import os
import shutil

from dotenv import load_dotenv


def move_func(src_folder, dst_folder):
    """
    Функция переносит файлы и папки и возвращает их количество
    """
    count_move_files = 0
    src_list_of_files = os.listdir(src_folder)

    if src_list_of_files:
        print(f'Перенос файлов из {src_folder} в папку {dst_folder}')
        for file in src_list_of_files:
            shutil.move(os.path.join(src_folder, file), os.path.join(dst_folder, file))
            print(f'{src_folder}{file} перенесен')
            count_move_files += 1
    else:
        print(f'Нечего переносить из {src_folder}')
    return count_move_files


def clear_old_func(dst_folder):
    """
    Функция удаляет старые файлы из папки хранилища и возвращает
    статистику операции
    """
    count_del_files = 0
    count_del_errors = 0
    count_del_folders = 0
    count_array = []
    dst_list_of_files = os.listdir(dst_folder)
    for file in dst_list_of_files:
        current_path_file = os.path.join(dst_folder, file)
        date_of_creating_file = datetime.datetime.fromtimestamp(
            os.path.getmtime(current_path_file)
        )
        if datetime.datetime.now() - date_of_creating_file > datetime.timedelta(weeks=27):
            print(f'Удаляем {file} {date_of_creating_file}')
            try:
                os.remove(current_path_file)
                count_del_files += 1
                print('DONE!')
            except OSError as error:
                print(error)
                print("Не удаётся удалить как файл")
                print("Попытка удалить как папку")
                try:
                    shutil.rmtree(
                        current_path_file, ignore_errors=True, onerror=None
                    )
                    print("DONE!")
                    count_del_folders += 1
                except OSError as error:
                    print(error)
                    print("Не удаётся удалить папку")
                    count_del_errors += 1
    return (count_del_files, count_del_folders, count_del_errors,)


if __name__ == '__main__':
    load_dotenv()
    src_folder = os.getenv('SOURCE')  # папка источник
    dst_folder = os.getenv('DESTINATION')  # папка приёмник
    time_now = datetime.date.today().strftime("%d.%m.%Y")

    print(f'сегодня {time_now}')
    value_of_moved = move_func(src_folder, dst_folder)
    statistic_del_operation = clear_old_func(dst_folder)

    print(f'Перенесено из папки {src_folder} {value_of_moved} файлов и папок')
    print(f'Удалено из папки {dst_folder} {statistic_del_operation[0]} '
          f'файлов и {statistic_del_operation[1]} папок')
    print(f'ошибок в удалении {statistic_del_operation[2]}')
