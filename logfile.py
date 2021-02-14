import datetime, configparser


class LogFile:

    def __init__(self):
        self.config = configparser.ConfigParser()

        self.config.read('config.ini')
        self.dtime = datetime.date.today()
        self.file_name = f'bu_log_{self.dtime.isoformat()}'




    def start_read_log(self):
        with open(self.file_name, 'w') as file:
            file.write('####### START LOGFILE #######\n')
            self.config.write(file)
            file.write(f'\ncurrent_time = {datetime.datetime.now().isoformat()}\n\n')
        with open(self.file_name, 'a') as file:
            file.write('####### START READING #######\n')
            file.write(f'\ncurrent_time = {datetime.datetime.now().isoformat()}\nfollowing files will not be copied\n')

    def logging_read_files(self, path):
        with open(self.file_name, 'a') as file:
           file.write(f'File or Directories: {path}\n')

    def start_directory_log(self):
        with open(self.file_name, 'a') as file:
            file.write('\n\n####### START CREATING DIRECTORIES #######\n')
            file.write(f'\ncurrent_time = {datetime.datetime.now().isoformat()}\nfollowing were not created\n')

    def logging_directory_log(self, path):
        with open(self.file_name, 'a') as file:
           file.write(f'File or Directories: {path}\n')

    def start_copy_log(self):
        with open(self.file_name, 'a') as file:
            file.write('\n\n####### START COPY #######\n')
            file.write(f'\ncurrent_time = {datetime.datetime.now().isoformat()}\nfollowing errors occured while copying\n')

    def logging_copy_log(self, source_path, traget_path):
        with open(self.file_name, 'a') as file:
            file.write(f'from :\t{source_path}\nto:\t\t{traget_path}\n')

    def summary(self, summary_string):
        with open(self.file_name, 'a') as file:
            summary = summary_string.replace("\t", "")
            file.write(f'\n\n\n{summary}')
            file.write(f'\ncurrent_time = {datetime.datetime.now().isoformat()}\n')

    def permission_denied(self,path):
        with open(self.file_name, 'a') as file:
            file.write(f'Permission denied: {path}\n')