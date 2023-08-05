from apscheduler.schedulers.background import BackgroundScheduler
import requests
from srmapstudents.config import apiUrl

def update():
    platforms = ['codechef', 'github', 'codeforces', 'leetcode']
    for platform in platforms:
        requests.get(f"{apiUrl}/srmapstudents/{platform}/")
    

def schedule():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update, "interval", days=7)
    scheduler.start()
