#!/usr/bin/env python3

import datetime
import os
import shutil


def move_func(src_f, dst_f, count_move):
    """
    Функция переносит файлы и папки и возвращает их количество
    """
    if src:
        print(f'Перенос файлов из {src_f} в папку {dst_f}')
        for file in src:
            shutil.move(os.path.join(src_f, file), os.path.join(dst_f, file))
            print(f'{src_f}{file} перенесен')
            count_move += 1
    else:
        print(f'Нечего переносить из {src_f}')
    return count_move


def clear_old_func(dst_r, dst_f, count, count_f, count_er):
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


if __name__ == '__main__':
    src_f = r'/home/boyko-ab/Рабочий стол/to_work'  # папка источник
    dst_f = '/home/boyko-ab/mnt/myfolder/work'  # папка приёмник
    src = os.listdir(src_f)  # список файлов во временной папке to_work
    dst_r = os.listdir(dst_f)  # список файлов в папке work
    now = datetime.date.today().strftime("%d.%m.%Y")  # сегодняшнее число
    count = 0  # счетчик для удаленных файлов
    count_er = 0  # счетчик ошибок при удалении
    count_f = 0  # счетчик удаленных папок
    count_move = 0  # счетчик перенесенных из  паки "протей" в папку "ворк"

    print(f'сегодня {now}')
    print_count = move_func(src_f, dst_f, count_move)
    print_array = clear_old_func(dst_r, dst_f, count, count_f, count_er)

    print(f'перенесено из папки {src_f} {print_count} файлов и папок')
    print(f'удалено из папки {dst_f} {print_array[0]} '
          f'файлов и {print_array[1]} папок')
    print(f'ошибок в удалении {print_array[2]}')
