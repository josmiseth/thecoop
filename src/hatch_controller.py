
import sys
sys.path.append('/home/pi/projects/thecoop/')

from apscheduler.schedulers.background import BackgroundScheduler

from src import test

print(sys.path)


def print_text():
    print("Scheduled event")
    
    return



sched = BackgroundScheduler()

sched.add_job(print_text, 'cron', minute='*')

sched.start()

