Installation:
	-extract the zip-file in the desired location.
	-to run python, the installation file python-3.9.1-amd64.exe is included
	-run "install_backup_bat.py", two .bat files will be created
	-in the windows autostart folder a shortcut to "main_autostart" must be created
		-at every Windows startup it checks how old the last backup is, and executes the code if necessary
		-if there is a current backup the program can only be started via "backup_manualstart.bat".


config.ini
	-[SOURCE] contains several paths of the directories to be copied
	-[Target] contains a path 'target' with the directory in which the backup should be created
	-[LAST_BACKUP] 'date' contains the date of the last backup in iso format, if no backup has been created yet it contains a default value
	-[AUTO_BACKUP]  : 'value' contains a Boolean, if the value is set to False the backup will not be started automatically after the analysis of the source directories
		              : 'interval_days' is an int-value with the number of days between two backups. Only after this time the program opens automatically on Windows startup
