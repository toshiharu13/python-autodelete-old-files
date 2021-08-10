#!/usr/bin/env python3

import os, shutil, datetime

src_p = r'/home/boyko-ab/Рабочий стол/to_work'  # папка источник
dst_f = '/home/boyko-ab/mnt/myfolder/work'  # папка приёмник
src = os.listdir(src_p)  # список файлов во временной папке to_work
dst_r = os.listdir(dst_f) # список файлов в папке work
now = datetime.date.today().strftime("%d.%m.%Y") # сегодняшнее число
count = 0 # счетчик для удаленных файлов
count_er = 0 # счетчик ошибок при удалении
count_f = 0 #счетчик удаленных папок
count_move = 0 # счетчик перенесенных из  паки "протей" в папку "ворк"
print(f'сегодня {now}')
if src:
    print('Перенос файлов из папки to_work в папку work')
    for file in src:
        shutil.move(os.path.join(src_p, file), os.path.join(dst_f, file))
        print(src_p+file)
        count_move += 1
else:
    print('No files to remove in \"to_work\" folder')
for file in dst_r:
    curpath = os.path.join(dst_f, file) # полный путь к обрабатываему файлу
    file_mod = datetime.datetime.fromtimestamp(os.path.getmtime(curpath)) # дата поледней модификации в нормальном виде
    if datetime.datetime.now() - file_mod > datetime.timedelta(weeks=27):
        print(f'{file} {file_mod} DELETING!')
        try:
            os.remove(curpath)
            count += 1
            print('DONE!')
        except OSError as error:
            #count_er += 1
            print(error)
            print("File can not be removed")
            print("try to delete as folder")
            try:
                shutil.rmtree(curpath, ignore_errors=True, onerror=None)
                print("DONE!")
                count_f += 1
            except OSError as error:
                print(error)
                print("Folder can not be removed")
                count_er += 1

print('перенесено из папки to_work', count_move)
print('удалено из папки work', count, 'файлов',',', count_f, "папок,")
print('ошибок в удалении', count_er)
