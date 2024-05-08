# Imported Modules
import time
from pushover import pushover_app
from gmail import gmail_app

def start_timer():
    start_time = time.time()
    return start_time

def end_timer_in_minutes(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_in_minutes = elapsed_time/60
    return elapsed_time_in_minutes

def end_timer_in_seconds(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def coffee_pushover_notifier():
    user_key = "utcd12k537bsjcax6w2i71exe4t39t"
    api_token = "ars2yhwu4euahs33hsyqj7j9bzy8td"
    pushover_notification = pushover_app.PushoverNotification(user_key, api_token)
    notification_content = "Ditt kaffe börjar bli kallt."
    pushover_notification.send_msg(notification_content)

def coffee_mail_notifier(msg):
    notifier = gmail_app.EmailNotification("kaffe.alert@gmail.com", "drpbnzkgiudlgngv")
    notifier.send_email(to="tomtelav@gmail.com",subject="Din veckoliga rapport!",body=msg)
