#!/usr/bin/env python3

import os, shutil, datetime
#import datetime

src_p = '/home/boyko-ab/Desktop/protei/' # откуда
dst = '/mnt/myfolder/work' # куда
src = os.listdir(src_p) # список файлов во временной папке protei
dst_r = os.listdir(dst) # список файлов в папке work
now = datetime.date.today().strftime("%d.%m.%Y") # сегодняшнее число
count = 0 # счетчик для удаленных файлов
count_er = 0 # счетчик ошибок при удалении
count_f = 0 #счетчик удаленных папок
print('сегодня',now)
if src:
	for file in src:
		shutil.move(os.path.join(src_p,file), os.path.join(dst,file))
		print(src_p+file)
else:
	print('No files to remove in \"Protei\" folder')
for file in dst_r:
	curpath = os.path.join(dst, file) # полный путь к обрабатываему файлу
	file_mod = datetime.datetime.fromtimestamp(os.path.getmtime(curpath)) # дата поледней модификации в нормальном виде
	if datetime.datetime.now() - file_mod > datetime.timedelta(weeks=27):
		print(file, file_mod, "DELETING!")
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
			except OSError  as error:
				print(error)
				print("Folder can not be removed")
				count_er += 1

print('удалено', count, 'файлов',',', count_f, "папок," , 'ошибок в удалении', count_er)
