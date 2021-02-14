Installation:
	-entpacke die zip-datei im gewünschten Ort
	-zum ausführen wird python benötigt, die Installationsdatei python-3.9.1-amd64.exe ist enthalten
	-"install_backup_bat.py" ausführen, zwei .bat-Dateien werden erstallt
	-in dem Windowsautostartordner muss eine Verknüpfung zu "main_autostart" erstellt werden
		-bei jedem Windows-start wird überprüft wie alt das letzte Backup ist, und der code gegebenfalls ausgeführt
		-wenn es ein aktuelles Backup gibt kann das Programm nur über "backup_manualstart.bat"


config.ini
	-[SOURCE] enthält mehrere Pfade der zu kopierenden Verzeichnisse
	-[Target] enthält einen Pfad 'ziel' mit dem Verzeichniss in dem das Backup erstellt werden soll
	-[LAST_BACKUP] 'date' enthält das Datum des letzten Backups im Isoformat, sollte noch kein Backup erstellt wurden sein enthält es einen Standartwert
	-[AUTO_BACKUP]	: 'value' enthält einen Boolean, ist der Wert auf False gestellt wird das Backup nicht automatisch nach der Analyse der Sourceverzeichnisse 					gestartet
			: 'interval_days' ist ein int-value mit der Anzahl der Tage zwischen zwei Backups. Erst nach dieser Zeit öffnet sich das Programm automatisch bei 				Windowsstart
