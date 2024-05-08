# Imorted modules
from flask import Flask, render_template, request
import actions
import threading
import datetime
import time
import psutil

coffee_app = Flask(__name__)

# Global variables
current_temperature = 0
prior_temperature = 0
coffee_counter = 0
coffee_machine_on = False

# Route for the home page, renders the index.html template.
@coffee_app.route("/")
def home():
    return render_template("index.html")

# Route for sending temperature
@coffee_app.route("/update_temperature", methods=["POST"])
def process_temperature_update():
    global current_temperature # float
    global prior_temperature # float
    global coffee_machine_on # bool
    global coffee_counter # int

    # Receive temperature and convert into a float.
    data = request.json
    current_temperature = float(data["temperature"])
    print("Received temperature:", current_temperature)
    
    # Starts timer -> coffee machine is on.
    if current_temperature >= 40 and coffee_machine_on == False:
        start_time = actions.start_timer()
        coffee_machine_on = True
        coffee_counter += 1 

    # Ends timer -> the coffee has cooled down.
    if current_temperature < 40 and coffee_machine_on == True:
        time = actions.end_timer_in_minutes(start_time)
    
    # Triggered if: user forgot coffee -> sends pushover notification.
    if prior_temperature >= 40 and current_temperature < 40 and time >= 50:
        actions.coffee_pushover_notifier()
        start_time = 0
        coffee_machine_on = False
    # Triggered if: user remembered coffee.
    elif prior_temperature >= 40 and current_temperature < 40 and time <= 50:
        start_time = 0
        coffee_machine_on = False
    else:
        print(f"Prior temperature: {prior_temperature}, New temperature: {current_temperature}")
    
    prior_temperature = current_temperature
    response = "Temperature received successfully"
    return response

# Route to retrieve the current temperature.
@coffee_app.route("/get_temperature")
def get_current_temperature():
    global current_temperature
    return {"temperature": current_temperature}

# Sends a weekly coffee usage alert notification Sunday at 8:00 PM and resets the coffee counter.
def coffee_weekly_alert():
    global coffee_counter
    while True:
        now = datetime.datetime.now()
        if now.weekday() == 6 and now.hour == 20 and now.minute == 0:
            actions.coffee_mail_notifier(f"You've made coffee {coffee_counter} times this week!")
            coffee_counter = 0
            time.sleep(60)
        else:
            time.sleep(10)

# Starts the Flask server.
if __name__ == "__main__":
    mail_thread = threading.Thread(target=coffee_weekly_alert)
    mail_thread.start()
    coffee_app.run(host="0.0.0.0")