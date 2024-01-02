#!/usr/bin/python3

import time
import datetime
from suntime import Sun, SunTimeException
import calendar

from apscheduler.schedulers.background import BackgroundScheduler


def close_hatch():
    print("Close hatch")
    return

def open_hatch():
    print("Open hatch")
    return


latitude = 63.446827
longitude = 10.421906

sun = Sun(latitude, longitude)

print("Adding cron job")
sched = BackgroundScheduler()
sched.add_job(open_hatch, 'cron', hour=9, minute=0)

#Setting up dates times for sunset for all days in a leap year (2024)
for month in range(1,13):
    for day in range(1,calendar.monthrange(2024, month)[1]+1):
        date = datetime.date(2024, month, day)
        sunset = sun.get_local_sunset_time(date)
        sunset_plus_one_hour = sunset + datetime.timedelta(hours=1)
        hour = sunset_plus_one_hour.strftime('%H')
        minute = sunset_plus_one_hour.strftime('%M')

        sched.add_job(close_hatch, 'cron', month=month, day=day, hour=hour, minute=minute)


sched.print_jobs()

print("Starting cron job")
sched.start()


try:
    print("sleep")
    while True:
        time.sleep(10)


finally:
    print("clean up")


sched.shutdown()
