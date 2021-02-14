

class Status:

    def __init__(self):
        self.directory_finished = False
        self.directory_error_count = 0
        self.directory_created_amount = 0
        self.files_copied = 0
        self.files_amount = 0
        self.files_error_count = 0
        self.show = 0
        self.finished_paths = 0
        self.permission_denied = 0
        self.hard_drive_space = 0
        self.backup_size = 0
        self.copied_space = 0

    # def show_status(self):
    #     increment = 1000  #int(self.files_amount/10)
    #     if self.show%increment == 0 or self.files_amount == self.files_copied:
    #         os.system('cls')
    #         if self.directory_finished:
    #             print(f'Directories finished')
    #         else:
    #             print('Directories will be created')
    #         print(f'Folder Error : \t\t{self.directory_error_count}')
    #         print(f'File Error : \t\t{self.files_error_count}')
    #         print(f'Directories created : \t{self.directory_created_amount}')
    #         print(f'Permission denied : \t{self.permission_denied}')
    #         print(f'Files copied : \t\t{self.files_copied}/{self.files_amount}')
    #         print(f'Copied space : \t{self.copied_space // 2**20} mb')
    #         print(f'Hard drive : \t\t{self.hard_drive_space} mb')
    #         print(f'Backup size : \t\t{self.backup_size} mb')

        self.show += 1

    def copied(self):
        self.files_copied += 1

    def dir_errors(self):
        self.directory_error_count += 1

    def file_errors(self):
        self.files_error_count += 1

    def directory_created(self):
        self.directory_created_amount += 1

    def permission_denied_func(self):
        self.permission_denied += 1
