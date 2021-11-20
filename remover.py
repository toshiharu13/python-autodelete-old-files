#!/usr/bin/env python3

import datetime
import os
import shutil

from dotenv import load_dotenv


def move_func(src_f, dst_f, src_list_of_files):
    """
    Функция переносит файлы и папки и возвращает их количество
    """
    count_move_files = 0
    if src_list_of_files:
        print(f'Перенос файлов из {src_f} в папку {dst_f}')
        for file in src_list_of_files:
            shutil.move(os.path.join(src_f, file), os.path.join(dst_f, file))
            print(f'{src_f}{file} перенесен')
            count_move_files += 1
    else:
        print(f'Нечего переносить из {src_f}')
    return count_move_files


def clear_old_func(dst_r, dst_f):
    """
    Функция удаляет старые файлы из папки хранилища и возвращает
    статистику операции
    """
    count_del_files = 0
    count_del_errors = 0
    count_del_folders = 0
    count_array = []
    for file in dst_r:
        # полный путь к обрабатываему файлу
        curpath = os.path.join(dst_f, file)
        # дата поледней модификации в нормальном виде
        file_mod = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
        if datetime.datetime.now() - file_mod > datetime.timedelta(weeks=27):
            print(f'Удаляем {file} {file_mod}')
            try:
                os.remove(curpath)
                count_del_files += 1
                print('DONE!')
            except OSError as error:
                print(error)
                print("Не удаётся удалить как файл")
                print("Попытка удалить как папку")
                try:
                    shutil.rmtree(curpath, ignore_errors=True, onerror=None)
                    print("DONE!")
                    count_del_folders += 1
                except OSError as error:
                    print(error)
                    print("Не удаётся удалить папку")
                    count_del_errors += 1
    count_array.append(count_del_files)
    count_array.append(count_del_folders)
    count_array.append(count_del_errors)
    return count_array


if __name__ == '__main__':
    load_dotenv()
    src_folder = os.getenv('SOURCE')  # папка источник
    dst_folder = os.getenv('DESTINATION')  # папка приёмник
    src_list_of_files = os.listdir(src_folder)  # список файлов в папке источник
    dst_list_of_files = os.listdir(dst_folder)  # список файлов в папке приёмник
    time_now = datetime.date.today().strftime("%d.%m.%Y")

    print(f'сегодня {time_now}')
    value_of_moved = move_func(src_folder, dst_folder, src_list_of_files)
    statistic_del_operation = clear_old_func(dst_list_of_files, dst_folder)

    print(f'перенесено из папки {src_folder} {value_of_moved} файлов и папок')
    print(f'удалено из папки {dst_folder} {statistic_del_operation[0]} '
          f'файлов и {statistic_del_operation[1]} папок')
    print(f'ошибок в удалении {statistic_del_operation[2]}')
