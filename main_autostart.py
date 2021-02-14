import configparser
import datetime
import UI


date = datetime.date.today()

config = configparser.ConfigParser()
config.read('config.ini')

last_date = config['LAST_BACKUP']['date']
last_date = datetime.date.fromisoformat(last_date)
time_diff = (date - last_date).days
print(time_diff)

if time_diff >= int(config['AUTO_BACKUP']['interval_days']):
    ui = UI.UserInterface()
