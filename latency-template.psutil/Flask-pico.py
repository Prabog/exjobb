# Wi-Fi libraries
import network

# Flask libraries
import urequests
import ujson

# Sensor libraries
import machine
import onewire, ds18x20

# Monitor libraries
import utime

# Misc libraries
import time
import gc

def connect_to_wifi():
    # WiFi and network settings
    SSID = "imel 1g"
    PASSWORD = "96902341"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("waiting to connect...")
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3: # If the wlan status isn't CYW43_LINK_UP
        raise RuntimeError("network connection failed")
    else:
        print("connected")
        status = wlan.ifconfig()
        print("ip = " + status[0])

# Read from DS18B20 temperature sensor.
def read_temperature():
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    roms = ds_sensor.scan()  # Scan for ROMs inside the loop
    for rom in roms:
        pass
    tempC = ds_sensor.read_temp(rom)
    return tempC, roms  # Return temperature and ROMs

# Used in loop to calculate latency.
total_latency = 0

def send_temperature():
    global total_latency

    # Reads the current temperature and prepares 
    # it to be sent to the server for updating.
    temperature, roms = read_temperature()
    print("Current temperature:", temperature)
    url = "http://192.168.1.68:5000/update_temperature"
    payload = {"temperature": temperature}

    # Encode payload as JSON
    json_payload = ujson.dumps(payload)
    
    # Headers
    headers = {"Content-Type": "application/json"}

    # Times latency in milliseconds.
    start_time = utime.ticks_ms()
    response = urequests.post(url, data=json_payload, headers=headers)  # Pass JSON payload
    end_time = utime.ticks_ms()
    
    # Calculate latency
    latency = (end_time - start_time) / 1000
    total_latency += latency

    del json_payload  # Free up memory
    del payload  # Free up memory
    del response  # Free up memory
    del roms  # Free up memory

    gc.collect()  # Perform garbage collection

    return {"latency": latency}

if __name__ == "__main__":
    connect_to_wifi()

    # Set pin and find sensor
    ds_pin = machine.Pin(28)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    
    # Calculate average values
    loop_counter = 0

    # Main loop
    while True:
        try: 
            values = send_temperature()
            loop_counter += 1
            # Print current values
            print(f"Latency: {values['latency']} seconds")

            # Print current average values
            print(f"Average latency: {total_latency / loop_counter} seconds")
            print('-------------------------------------------------------')
            time.sleep(1)

        except KeyboardInterrupt:
            print("User ended the program.")
            break
