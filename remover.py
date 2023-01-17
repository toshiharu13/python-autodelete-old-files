#!/usr/bin/env python3

import datetime
import logging
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
        for file in src_list_of_files:
            shutil.move(os.path.join(src_folder, file), dst_folder)
            logging.info(f'{src_folder}{file} перенесен')
            count_move_files += 1

    return count_move_files


def clear_old_func(dst_folder):
    """
    Функция удаляет старые файлы из папки хранилища и возвращает
    статистику операции
    """
    count_del_files = 0
    count_del_errors = 0
    count_del_folders = 0
    dst_list_of_files = os.listdir(dst_folder)

    for file in dst_list_of_files:
        current_path_file = os.path.join(dst_folder, file)
        date_of_creating_file = datetime.datetime.fromtimestamp(
            os.path.getmtime(current_path_file))
        if datetime.datetime.now() - date_of_creating_file > datetime.timedelta(weeks=27):
            logging.info(f'Удаляем {file} {date_of_creating_file}')
            try:
                os.remove(current_path_file)
                count_del_files += 1
                logging.info('DONE!')
            except OSError as error:
                logging.info(f"Не удаётся удалить как файл - {error}. Попытка удалить как папку")
                try:
                    shutil.rmtree(
                        current_path_file, ignore_errors=True, onerror=None)
                    logging.info("DONE!")
                    count_del_folders += 1
                except OSError as error:
                    logging.info(f"Не удаётся удалить папку - {error}")
                    count_del_errors += 1
    return (count_del_files, count_del_folders, count_del_errors,)


def unmount(arm, mount_dest):
    """
    Размонтируем
    """
    try:
        os.system(f'sudo -S umount {mount_dest}')
        logging.info(f'Отключаемся от {arm}')
    except BaseException as ex:
        logging.error(f'Размантирование не удалось: {ex}')
        return ex


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s; %(levelname)s; %(name)s; %(message)s',
        filename='logs.log',
        filemode='w', )

    load_dotenv()
    src_folder = os.getenv('SOURCE')  # папка источник
    share_folder = os.getenv('DESTINATION')  # папка шары
    time_now = datetime.date.today().strftime("%d.%m.%Y")
    server = os.getenv('SERVER')
    user_name = os.getenv('USER_NAME')
    password = os.getenv('PASS')
    folder_in_share = os.getenv('REQUIREMENT_FOLDER')
    dst_folder = os.path.join(share_folder, folder_in_share)
    logging.info(f'сегодня {time_now}')

    os.system(f'sudo -S mount -t cifs //{server} {share_folder} --verbose -o user={user_name},password={password}')

    print(f'Перенос файлов из {src_folder} в папку {dst_folder}')
    value_of_moved = move_func(src_folder, dst_folder)
    if value_of_moved == 0:
        print(f'Нечего переносить из {src_folder}')

    statistic_del_operation = clear_old_func(dst_folder)

    print(f'Перенесено из папки {src_folder} {value_of_moved} файлов и папок')
    print(f'Удалено из папки {dst_folder} {statistic_del_operation[0]} '
          f'файлов и {statistic_del_operation[1]} папок')
    print(f'ошибок в удалении {statistic_del_operation[2]}')

    unmount(server, share_folder)




