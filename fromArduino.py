from datetime import datetime

import serial
import asyncio
import aiohttp

async def send_request(url, data):
    try:
        timeout = aiohttp.ClientTimeout(total=5)  # Set the timeout to 5 seconds
        async with aiohttp.ClientSession() as session:
            print(f"Sending request to {url}")
            async with session.post(url, data=data, timeout=timeout) as response:
                print(f"Request sent to {url}")
    except:
        print(f"Request to {url} failed")


def main():
    # Replace 'COM3' with your Arduino port
    arduino_port = '/dev/ttyACM0'
    baud_rate = 9600
    base_url = "http://intensif05.ecole.ensicaen.fr:8080/"
    route_warning = "soundWarning"
    route_police = "soundPoliceAlert"
    route_warning = "api/sound/reduceScore"
    route_police = "api/sound/reduceScore"
    id_device = "1"

    number_of_seconds_since_loud_sound = 0
    number_of_seconds_since_silence = 0
    number_of_seconds_before_warning = 2
    number_of_seconds_before_reset = 2
    number_of_seconds_before_police = 5
    warned = False
    police_sent = False

    try:
        arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to {arduino_port} at {baud_rate} baud")

        while True:
            data = arduino.readline().decode('utf-8').strip()
            #print(f"Arduino says: {data}")
            if("1" in data):
                current_time = datetime.now().hour
                if current_time > 22 or current_time < 7:
                    multiplicateur = 1
                else:
                    multiplicateur = 0.5
                number_of_seconds_since_silence = 0
                number_of_seconds_since_loud_sound += multiplicateur
                if not warned and number_of_seconds_since_loud_sound > number_of_seconds_before_warning:
                    print("WARNING: Loud sound detected for more than 10 seconds!")
                    asyncio.run(send_request(base_url + route_warning, {"id_user": id_device, "message": "WARNING: Loud sound detected for more than 10 seconds!"}))
                    warned = True
                if not police_sent and number_of_seconds_since_loud_sound > number_of_seconds_before_police:
                    print("WARNING: Police have been notified!")
                    number_of_seconds_since_loud_sound = 0
                    asyncio.run(send_request(base_url + route_police, {"id_user": id_device, "message": "WARNING: Police have been notified!"}))
                    police_sent = True

            else:
                if number_of_seconds_since_loud_sound != 0:
                    number_of_seconds_since_silence += 1
                    if number_of_seconds_since_silence > number_of_seconds_before_reset:
                        print("Resetting...")
                        number_of_seconds_since_loud_sound = 0
                        number_of_seconds_since_silence = 0
                        warned = False
                        police_sent = False

            """if("Avertissement" in data):
                print("WARNING: Loud sound detected for more than 10 seconds!")
                # send a warning to the server via a POST request
                content = {"id_device": id_device, "message": "WARNING: Loud sound detected for more than 10 seconds!"}
                sendMessageToServer(base_url + "soundWarning", content)
    
            elif("Police" in data):
                print("WARNING: Police have been notified!")
                # send a warning to the server via a POST request
                content = {"id_device": id_device, "message": "WARNING: Police have been notified!"}
                sendMessageToServer(base_url + "policeWarning", content)"""

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        if arduino.is_open:
            arduino.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()
