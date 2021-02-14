import Space_information
import configparser
import datetime
import os
import shutil
import status
import threading
from tkinter import *
import logfile


class UserInterface:

    def __init__(self):
        self.ui = Tk('Backup-Manager')
        self.ui.title('Backup-Manager')
        self.ui.config(padx=25, pady=25)
        self.source_lst = []
        self.last_backup = ''

        self.current_config = Text(width=50, height=20)
        self.current_config.grid(row=1, column=0, pady=10, padx=10)

        # button show config
        self.button_show_config = Button(text='show current config', command=self.get_config, pady=5)
        self.button_show_config.grid(row=0, column=0)

        # button scan directories
        self.button_start = Button()
        self.button_find_data = Button(text='Find files to copy',
                                       command=threading.Thread(target=self.find_resources).start)
        self.button_find_data.grid(row=0, column=1)

        # button start backup
        self.button_start.config(text='Start Backup', state=DISABLED,
                                 command=threading.Thread(target=self.backup_routine).start)
        self.button_start.grid(row=2, column=0, columnspan=2)

        # textfield of backup status
        self.current_status = Text(width=50, height=20, bg='white')
        self.current_status.grid(row=1, column=1, pady=10)

        # textfield of program status
        self.program_status = Text(width=50, height=1, bg='green')
        self.program_status.grid(row=10, column=0, pady=10, columnspan=2)

        # date
        self.date = datetime.date.today()
        self.date_str = self.date.isoformat()

        self.auto_backup = bool
        self.config_lst = {}
        self.file_list = {}
        self.bu_list = {}
        self.target = ''
        self.summary_string = ''

        self.button_settings = Button(text='Settings', command=self.open_settings)
        self.button_settings.grid(row=0, column=3)

        self.log = logfile.LogFile()

        self.status = status.Status()
        self.show_status_bu()
        self.get_config()
        self.backup_needed()
        self.ui.mainloop()

    def show_status_bu(self):
        status_string = ''
        status_string += f'Folder Error :\t\t\t{self.status.directory_error_count}\n'
        status_string += f'File Error :\t\t\t{self.status.files_error_count}\n'
        status_string += f'Directories created :\t\t\t{self.status.directory_created_amount}\n'
        status_string += f'Permission denied :\t\t\t{self.status.permission_denied}\n'
        status_string += f'Files copied :\t\t\t{self.status.files_copied}/{self.status.files_amount}\n'
        status_string += f'Copied space:\t\t\t{self.status.copied_space // 2 ** 20} mb\n'
        status_string += f'Hard drive space: \t\t\t{self.status.hard_drive_space} mb\n'
        status_string += f'Backup size: \t\t\t{self.status.backup_size} mb\n'
        self.summary_string = status_string
        self.current_status.delete(1.0, END)
        self.current_status.insert(1.0, status_string)
        self.ui.after(100, func=self.show_status_bu)

    def get_config(self):
        self.config_lst = configparser.ConfigParser()
        self.config_lst.read('config.ini')

        label_text = ''
        label_text += '[SOURCES]\n'
        i = 0
        for key in self.config_lst['SOURCE']:
            i += 1
            label_text += f"Path{i} = {self.config_lst['SOURCE'][key]}\n"

        label_text += '\n[Target]\n'

        if self.config_lst['AUTO_BACKUP']['value'] == 'True':
            self.auto_backup = True
        else:
            self.auto_backup = False

        for key in self.config_lst['TARGET']:
            self.target = self.config_lst['TARGET'][key]
            label_text += f"Path = {self.config_lst['TARGET'][key]}\n"

        label_text += '\n[LAST_BACKUP]\n'
        i = 0
        for key in self.config_lst['LAST_BACKUP']:
            i += 1
            label_text += f"Date{i} = {self.config_lst['LAST_BACKUP'][key]}\n"
            self.last_backup = datetime.date.fromisoformat(self.config_lst['LAST_BACKUP'][key])

        label_text += f'\n[AUTO_BACKUP]\n'
        label_text += f"value = {self.config_lst['AUTO_BACKUP']['value']}\n"
        label_text += f"interval_days = {self.config_lst['AUTO_BACKUP']['interval_days']}"

        self.source_lst = [r"{}".format(self.config_lst['SOURCE'][i]) for i in self.config_lst['SOURCE']]
        self.current_config.delete(1.0, END)
        self.current_config.insert(1.0, label_text)

    def backup_needed(self):
        timedelta = self.date - self.last_backup

        if timedelta.days >= int(self.config_lst['AUTO_BACKUP']['interval_days']):
            self.label_backup_needed = Label(self.ui, text=f"Last backup is older than "
                                                           f"{self.config_lst['AUTO_BACKUP']['interval_days']} days"
                                                           f"\nNEW BACKUP IS URGENT", bg='red', width=50, height=5)
        else:
            self.label_backup_needed = Label(self.ui, text='Last backup is not older than 2 weeks',
                                             bg='green', width=50, height=5)
        self.label_backup_needed.grid(row=12, column=0, columnspan=2)

    ########################################### FIND FILES ############################################

    def find_resources(self):
        self.disable_buttons()
        self.log.start_read_log()
        self.get_config()
        for path in self.source_lst:  # all source paths
            self.file_list[path] = []
            self.bu_list[path] = []
            item_lst = os.listdir(path)
            for i in range(len(item_lst)):  # list content
                item_lst[i] = path + '/' + item_lst[i]
                if os.path.isfile(item_lst[i]):
                    self.file_list[path].append(item_lst[i])
                elif os.path.isdir(item_lst[i]):
                    self.find_all_recursiv(item_lst[i], path)
        self.get_memory_spaces()

        self.enable_buttons()
        if self.auto_backup:
            self.backup_routine()

    def find_all_recursiv(self, cur_directory, path):
        try:
            dir_content = os.listdir(cur_directory)
            for i in range(len(dir_content)):
                dir_content[i] = cur_directory + '/' + dir_content[i]
                try:
                    if os.path.isfile(dir_content[i]):
                        self.file_list[path].append(dir_content[i])
                        self.status.files_amount += 1
                    elif os.path.isdir(dir_content[i]):
                        self.find_all_recursiv(dir_content[i], path)
                except:
                    self.status.file_errors()
                    self.log.logging_read_files(dir_content[i])
        except PermissionError:
            self.status.permission_denied_func()
            self.log.permission_denied(cur_directory)
        except:
            self.status.file_errors()
            self.log.logging_read_files(cur_directory)
    ############################### BACKUP ##############################################

    def backup_routine(self):
        self.disable_buttons()
        if self.status.backup_size*1.2 < self.status.hard_drive_space:
            self.setting_target_directories()
            self.creating_directories()
            self.copy_files()
            self.set_current_date()
            self.after_backup()
        else:
            self.program_status.delete(1.0, END)
            self.program_status.insert(1.0, f'Harddrive space is low, {self.status.backup_size}, {self.status.hard_drive_space}')
            self.program_status.config(bg='red')

    def setting_target_directories(self):
        for key in self.file_list:
            for file in self.file_list[key]:
                new_filepath = self.target + r'/' + self.date_str + r'/' + key.split(r'/')[-1]
                file_path = file.split(r'/')
                source_path = key.split(r'/')
                for i in range(len(file_path)):
                    for j in range(len(source_path)):
                        if i == j and source_path[j] == file_path[i]:
                            file_path[i] = ''
                            continue

                for i in file_path:
                    if not i == '':
                        new_filepath += r'/' + i

                new_filepath = new_filepath.split(r'/')
                new_filepath.pop()
                new_filepath = r'/'.join(new_filepath)

                self.bu_list[key].append(new_filepath)

    def creating_directories(self):
        self.log.start_directory_log()
        for key in self.file_list:
            for i in range(len(self.file_list[key])):
                target_path = self.bu_list[key][i]
                try:
                    os.makedirs(target_path)
                    self.status.directory_created()
                except:
                    if not os.path.isdir(target_path):
                        self.status.dir_errors()
                        self.log.logging_directory_log(target_path)

    def copy_files(self):
        self.log.start_copy_log()
        for key in self.file_list:
            for i in range(len(self.file_list[key])):
                source_path = self.file_list[key][i]
                target_path = self.bu_list[key][i]
                try:
                    shutil.copy2(source_path, target_path)
                    self.status.copied()
                    self.status.copied_space += os.path.getsize(source_path)
                except:
                    self.status.file_errors()
                    self.log.logging_copy_log(source_path, target_path)

    ############################### functionalities ##############################################

    def get_memory_spaces(self):
        self.status.backup_size = Space_information.backup_size(self.file_list)
        self.status.hard_drive_space = Space_information.volume_free_space(self.target)

    def disable_buttons(self):
        self.button_find_data.config(state=DISABLED)
        self.button_show_config.config(state=DISABLED)
        self.button_start.config(state=DISABLED)
        self.program_status.delete(1.0, END)
        self.program_status.insert(1.0, 'Program working, Buttons disabled')
        self.program_status.config(bg='red')

    def enable_buttons(self):
        # self.button_find_data.config(state=NORMAL)
        self.button_show_config.config(state=NORMAL)
        self.button_start.config(state=NORMAL)
        self.program_status.delete(1.0, END)
        self.program_status.insert(1.0, 'last work done, Buttons enabled')
        self.program_status.config(bg='green')

    def after_backup(self):
        self.button_show_config.config(state=NORMAL)
        # self.button_start.config(state=NORMAL)
        self.program_status.delete(1.0, END)
        self.program_status.insert(1.0, 'backup done')
        self.program_status.config(bg='green')
        self.label_backup_needed.configure(text='backup done', bg='green')
        self.log.summary(self.summary_string)

    ############################### settings ##############################################

    def open_settings(self):
        self.settings = Tk()
        self.settings.title('Settings')
        self.settings.config(padx=25, pady=25)

        self.label_auto_backup = Label(self.settings, text=str(self.auto_backup))
        self.label_auto_backup.grid(row=0, column=1, pady=10)

        self.button_auto_backup = Button(self.settings, text='Change auto backup value', command=self.change_auto_backup,
                                         width=30)
        self.button_auto_backup.grid(row=0, column=0, padx=20, pady=10)

        self.button_clear_sources = Button(self.settings, text='delete current sources', command=self.clear_sources,
                                           width=30)
        self.button_clear_sources.grid(row=1, column=0, padx=20, pady=10)

        self.label_clear_sources = Label(self.settings)
        self.label_clear_sources.grid(row=1, column=1)

        self.button_add_source = Button(self.settings, text='add source path', command=self.add_source, width=30)
        self.button_add_source.grid(row=2, column=0, padx=20, pady=10)

        self.entry_add_source = Entry(self.settings)
        self.entry_add_source.grid(row=2, column=1, padx=20, pady=10)

        self.button_set_target = Button(self.settings, text='set Target', width=30, command=self.set_target)
        self.button_set_target.grid(row=3, column=0, padx=20, pady=10)

        self.entry_target = Entry(self.settings)
        self.entry_target.grid(row=3, column=1, padx=20, pady=10)

        self.settings.mainloop()

    def change_auto_backup(self):
        if self.auto_backup:
            self.auto_backup = False
        elif not self.auto_backup:
            self.auto_backup = True
        self.label_auto_backup.configure(text=str(self.auto_backup))
        self.config_lst['AUTO_BACKUP']['value'] = str(self.auto_backup)
        with open('config.ini', 'w') as file:
            self.config_lst.write(file)

    def clear_sources(self):
        self.config_lst['SOURCE'] = {}
        with open('config.ini', 'w') as file:
            self.config_lst.write(file)
        self.label_clear_sources.configure(text='Sources deleted')

    def add_source(self):
        new_path = fr'{self.entry_add_source.get()}'
        new_path = new_path.replace('\\', '/')
        i = 0

        for key in self.config_lst['SOURCE']:
            i += 1
        self.config_lst['SOURCE'][f'path{i}'] = new_path
        with open('config.ini', 'w') as file:
            self.config_lst.write(file)

    def set_current_date(self):
        self.config_lst['LAST_BACKUP']['date'] = self.date_str
        with open('config.ini', 'w') as file:
            self.config_lst.write(file)

    def set_target(self):
        new_target = fr'{self.entry_target.get()}'
        new_target = new_target.replace('\\', '/')
        self.config_lst['TARGET']['ziel'] = new_target

        with open('config.ini', 'w') as file:
            self.config_lst.write(file)
