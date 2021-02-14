import shutil, os, configparser, status, datetime, Space_information, time, UI
from tkinter import *

all_files = {}
bu_files = {}
backup_status = status.Status()
date = datetime.date.today()
date_str = date.strftime('%Y-%m-%d')

def find_all_start(source):
    global all_files, bu_files
    for path in source:  # alle Sourcepfade
        all_files[path] = []
        bu_files[path] = []
        item_lst = os.listdir(path)
        for i in range(len(item_lst)):  # anhalte auflisten
            item_lst[i] = path + '/' + item_lst[i]
            if os.path.isfile(item_lst[i]):
                all_files[path].append(item_lst[i])
            elif os.path.isdir(item_lst[i]):
                find_all_recursiv(item_lst[i], path)


def find_all_recursiv(dir,path):
    try:
        dir_content = os.listdir(dir)
        for i in range(len(dir_content)):  # anhalte auflisten
            dir_content[i] = dir + '/' + dir_content[i]
            try:
                if os.path.isfile(dir_content[i]):
                    all_files[path].append(dir_content[i])
                    backup_status.files_amount += 1
                    backup_status.show_status()
                elif os.path.isdir(dir_content[i]):
                    find_all_recursiv(dir_content[i],path)
            except:
                backup_status.file_errors()
    except PermissionError:
        backup_status.permission_denied_func()
    except:
        backup_status.file_errors()

def set_target_dir():
    global target, all_files
    for key in all_files:
        for file in all_files[key]:
            new_filepath = target + '/' + date_str + '/' + key.split('/')[-1]
            file_path = file.split('/')
            source_path = key.split('/')
            for i in range(len(file_path)):
                for j in range(len(source_path)):
                    if i == j and source_path[j] == file_path[i]:
                        file_path[i] = ''
                        continue

            for i in file_path:
                if not i == '':
                    new_filepath += '/' + i

            new_filepath = new_filepath.split('/')
            new_filepath.pop()
            new_filepath = '/'.join(new_filepath)

            bu_files[key].append(new_filepath)
            #print(bu_files[key])

def copy_all_files():
    global all_files, bu_files
    for key in all_files:
        for i in range(len(all_files[key])):
            backup_status.show_status()
            source_path = all_files[key][i]
            target_path = bu_files[key][i]
            try:
                shutil.copy2(source_path, target_path)
                backup_status.copied()
                backup_status.copied_space += os.path.getsize(source_path)

            except:
                print(f'ERROR: Target: {target_path}, Source: {source_path}')
                backup_status.file_errors()
        backup_status.finished_paths += 1

def create_directories():
    global all_files, bu_files
    for key in all_files:
        for i in range(len(all_files[key])):
            target_path = bu_files[key][i]
            try:
                os.makedirs(target_path)
                backup_status.directory_created()
            except:
                 if not os.path.isdir(target_path):
                     print(f'Error: Target: {target_path}')
                     backup_status.dir_errors()
            backup_status.show_status()


    backup_status.directory_finished = True


################## DIRECTORIES ##################

config = configparser.ConfigParser()
config.read('config.ini')
keys = config.sections()
sources = [config['SOURCE'][i] for i in config['SOURCE']] # liste aller Quellpfade
target = config['TARGET']['Ziel']
last_date=config['LAST_BACKUP']['date']
last_date = datetime.date.fromisoformat(last_date)
time_diff = (date - last_date).days
print(sources)
################## DIRECTORIES ##################


def backup_start():
    find_all_start(sources)
    backup_status.files_amount = 0
    for key in all_files:
        backup_status.files_amount += len(all_files[key])
    backup_size = Space_information.backup_size(all_files)  #required space
    backup_status.backup_size = backup_size
    free_space = Space_information.volume_free_space(target)  #available space
    backup_status.hard_drive_space = free_space

    if free_space > backup_size * 2:
        set_target_dir()

        create_directories()

        copy_all_files()

        backup_status.show_status()
        config['LAST_BACKUP']['date'] = date_str
        with open('config.ini','w') as file:
            config.write(file)
        input('current date overwrite')
    else:
        print('Target need more free space')

def user_input():
    user_input_value = input('Backup ist fällig! Soll es jetzt durchgeführt werden? [y/n]  ')
    if user_input_value == 'y':
        backup_start()
    else:
        time.sleep(4*3600)
        user_input()


ui = UI.UserInterface()

#ui.ui.mainloop()

#if time_diff >= 0:
#    user_input()
#
#