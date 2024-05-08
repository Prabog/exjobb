# Wi-Fi libraries
import network

# Flask libraries
import urequests

# Sensor libraries
import machine
import onewire, ds18x20

# Monitor libraries
import utime

# Misc libraries
import time

def connect_to_wifi():
    # WiFi and network settings
    SSID = "Biblioteket"
    PASSWORD = "alicekompis"
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

    # Return value of cyw43_wifi_link_status
    # define CYW43_LINK_DOWN (0)
    # define CYW43_LINK_JOIN (1)
    # define CYW43_LINK_NOIP (2)
    # define CYW43_LINK_UP (3)
    # define CYW43_LINK_FAIL (-1)
    # define CYW43_LINK_NONET (-2)
    # define CYW43_LINK_BADAUTH (-3)

    # Raspberry Pi Pico WiFi docs: https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf

# Read from DS18B20 temperature sensor.
def read_temperature():
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        pass
    tempC = ds_sensor.read_temp(rom)
    return tempC

# Used in loop to calculate latency.
total_latency = 0

def send_temperature():
    global total_latency

    # Reads the current temperature and prepares 
    # it to be sent to the server for updating.
    temperature = read_temperature()
    print("Current temperature:", temperature)
    url = "http://192.168.1.68:5000/update_temperature"
    payload = {"temperature": temperature}

    # Times latency in milliseconds.
    start_time = utime.ticks_ms()
    response = urequests.post(url, data=payload)
    end_time = utime.ticks_ms()

    # Calculate latency
    latency = (end_time - start_time) / 1000
    total_latency += latency

    del payload  # Free up memory
    del response  # Free up memory

    return {"latency": latency}

if __name__ == "__main__":
    connect_to_wifi()

    # Set pin and find sensor
    ds_pin = machine.Pin(28)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    print('Found DS devices: ', roms)

    # Used to calculate average values
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
            time.sleep(10)

        except KeyboardInterrupt:
            print("User ended the program.")
            break