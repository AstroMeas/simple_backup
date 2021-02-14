import os


working_directory = os.getcwd()
print(working_directory)
auto_backup = 'main_autostart.py'
manual_backup = 'main_manualstart.py'

with open('backup_autostart.bat', 'w') as auto:
    auto.write(rf"python {working_directory}\{auto_backup}")

with open('backup_manualstart.bat', 'w') as auto:
    auto.write(rf"python {working_directory}\{manual_backup}")

