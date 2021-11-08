#!/usr/bin/env python3

import datetime
import os
import shutil

from dotenv import load_dotenv


def move_func(src_f, dst_f, count_move, src_list_of_files):
    """
    Функция переносит файлы и папки и возвращает их количество
    """
    if src_list_of_files:
        print(f'Перенос файлов из {src_f} в папку {dst_f}')
        for file in src_list_of_files:
            shutil.move(os.path.join(src_f, file), os.path.join(dst_f, file))
            print(f'{src_f}{file} перенесен')
            count_move += 1
    else:
        print(f'Нечего переносить из {src_f}')
    return count_move


def clear_old_func(dst_r, dst_f, count, count_f, count_er):
    """
    Функция удаляет старые файлы из папки хранилища и возвращает
    статистику операции
    """
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
                count += 1
                print('DONE!')
            except OSError as error:
                print(error)
                print("Не удаётся удалить как файл")
                print("Попытка удалить как папку")
                try:
                    shutil.rmtree(curpath, ignore_errors=True, onerror=None)
                    print("DONE!")
                    count_f += 1
                except OSError as error:
                    print(error)
                    print("Не удаётся удалить папку")
                    count_er += 1
    count_array.append(count)
    count_array.append(count_f)
    count_array.append(count_er)
    return count_array


def mount(arm, user, passwd):
    """
    Монтируем АРМ по шаре C$
    """
    os.system(f'sudo -S mount -t cifs //{arm}/c$ /home/boyko-ab/mnt/logs2/ '
              f'--verbose -o user={user},password={passwd}')


def unmount(arm):
    """
    Размонтируем
    """
    os.system('sudo -S umount /home/boyko-ab/mnt/logs2/')
    print(f'Отключаемся от {arm}')


if __name__ == '__main__':
    load_dotenv()
    src_folder = os.getenv('SOURCE')  # папка источник
    dst_folder = os.getenv('DESTINATION')  # папка приёмник
    src_list_of_files = os.listdir(src_folder)  # список файлов во временной папке to_work
    dst_list_of_files = os.listdir(dst_folder)  # список файлов в папке work
    time_now = datetime.date.today().strftime("%d.%m.%Y")
    count_del_files = 0  # счетчик для удаленных файлов
    count_del_errors = 0  # счетчик ошибок при удалении
    count_del_folders = 0  # счетчик удаленных папок
    count_moved_to_dest = 0  # счетчик перенесенных из  паки "протей" в папку "ворк"


    print(f'сегодня {time_now}')
    value_of_moved = move_func(
        src_folder, dst_folder, count_moved_to_dest, src_list_of_files
    )
    statistic_del_operation = clear_old_func(
        dst_list_of_files, dst_folder, count_del_files, count_del_folders, count_del_errors
    )

    print(f'перенесено из папки {src_folder} {value_of_moved} файлов и папок')
    print(f'удалено из папки {dst_folder} {statistic_del_operation[0]} '
          f'файлов и {statistic_del_operation[1]} папок')
    print(f'ошибок в удалении {statistic_del_operation[2]}')
