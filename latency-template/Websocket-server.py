# Imported modules
import socket
import actions
import threading
import datetime
import time
import json

# Global variables
prior_temperature = 0
coffee_counter = 0
coffee_machine_on = False

def process_temperature_update():
    global prior_temperature
    global coffee_counter
    global coffee_machine_on

    try:
        while True:
            received_data = client_socket.recv(1024)
            if not received_data:
                break

            json_data = received_data.decode()
            data = json.loads(json_data)
            current_temperature = float(data["temperature"])
            print("Received temperature:", current_temperature)

            # Starts timer
            if current_temperature >= 40 and coffee_machine_on == False:
                start_time = actions.start_timer()
                coffee_machine_on = True
                coffee_counter += 1 

            # Ends timer
            if current_temperature < 40 and coffee_machine_on == True:
                time = actions.end_timer_in_minutes(start_time)
            
            # Sends a pushover notification
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
            client_socket.sendall(response.encode())

    except json.JSONDecodeError:
        print("Error decoding JSON data")

    finally:
        # Close the connection
        client_socket.close()

# Sends a gmail notifiacation
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

if __name__ == "__main__":
    mail_thread = threading.Thread(target=coffee_weekly_alert())
    mail_thread.start()

    # Specifies address family and socket type
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind(("0.0.0.0", 5001))

    # Specifies the amount of allowed clients
    server_socket.listen(1)

    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print("Connected to", client_address)
    print("Client socket", client_socket)

    process_temperature_update()