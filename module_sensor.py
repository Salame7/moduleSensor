import threading
import time
import requests
import math
import os
import subprocess
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from w1thermsensor import W1ThermSensor

# Configuracion global
stop_stream = False

# Sensor de sonido
def sensor_sonido():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan0 = AnalogIn(ads, ADS.P0)
    delayTime = 0.5
    offset_voltage = 1.24
    moderate_threshold = 1.30
    high_readings = 0
    start_time = time.time()
    reminder_time = time.time()
    reminder_interval = 30 * 60
    llanto_detectado = False

    correo_electronico = os.getenv("EMAIL", "default@example.com")
    endpoint = os.getenv("SOUND_ENDPOINT", "https://default-endpoint.com")

    while True:
        try:
            voltage = chan0.voltage
            if voltage > moderate_threshold:
                high_readings += 1

            if time.time() - start_time >= 60:
                if high_readings >= 10:
                    llanto_detectado = True
                    payload = {"correo_electronico": correo_electronico, "estado": 1}
                    requests.post(endpoint, json=payload)
                    reminder_time = time.time()
                elif llanto_detectado and high_readings == 0:
                    payload = {"correo_electronico": correo_electronico, "estado": 2}
                    requests.post(endpoint, json=payload)
                    llanto_detectado = False

                high_readings = 0
                start_time = time.time()

            if time.time() - reminder_time >= reminder_interval:
                payload = {"correo_electronico": correo_electronico, "estado": 3}
                requests.post(endpoint, json=payload)
                reminder_time = time.time()

            time.sleep(delayTime)
        except requests.exceptions.RequestException as e:
            print(f"Error en sensor de sonido: {e}")
        except Exception as e:
            print(f"Error inesperado en sensor de sonido: {e}")

# Sensor de temperatura
def sensor_temperatura():
    sensor = W1ThermSensor()
    reminder_interval = 5 * 60
    reminder_time = time.time()
    cold_alert_interval = 30
    hot_alert_interval = 30
    last_cold_alert_time = time.time()
    last_hot_alert_time = time.time()

    endpoint = os.getenv("TEMP_ENDPOINT", "https://default-endpoint.com")
    email = os.getenv("EMAIL", "default@example.com")

    while True:
        try:
            temperature = sensor.get_temperature()
            current_time = time.time()

            if temperature <= 18 and current_time - last_cold_alert_time >= cold_alert_interval:
                payload = {"correo_electronico": email, "nivel_temperatura": temperature, "estado": 2}
                requests.post(endpoint, json=payload)
                last_cold_alert_time = current_time

            if temperature >= 24 and current_time - last_hot_alert_time >= hot_alert_interval:
                payload = {"correo_electronico": email, "nivel_temperatura": temperature, "estado": 3}
                requests.post(endpoint, json=payload)
                last_hot_alert_time = current_time

            if current_time - reminder_time >= reminder_interval:
                payload = {"correo_electronico": email, "nivel_temperatura": temperature, "estado": 1}
                requests.post(endpoint, json=payload)
                reminder_time = current_time

            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error en sensor de temperatura: {e}")
        except Exception as e:
            print(f"Error inesperado en sensor de temperatura: {e}")

# Streaming de video
def stream_with_gstreamer():
    AWS_KEY_PUBLIC = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_KEY_PRIVATE = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    stream_name = os.getenv("STREAM_NAME", "test1")
    gstreamer_cmd = (
        f"gst-launch-1.0 libcamerasrc ! "
        f"video/x-raw,format=NV12,width=320,height=180,framerate=15/1 ! "
        f"queue leaky=2 max-size-time=0 max-size-buffers=2 max-size-bytes=0 ! "
        f"videoconvert ! videobalance saturation=0.0 ! "
        f"x264enc tune=zerolatency speed-preset=ultrafast bitrate=500 key-int-max=15 ! "
        f"video/x-h264,stream-format=avc,alignment=au ! "
        f"kvssink stream-name={stream_name} "
        f"aws-region={AWS_REGION} "
        f"access-key={AWS_KEY_PUBLIC} "
        f"secret-key={AWS_KEY_PRIVATE}"
    )

    try:
        process = subprocess.Popen(gstreamer_cmd, shell=True)
        while not stop_stream:
            time.sleep(1)
        process.terminate()
    except Exception as e:
        print(f"Error en streaming de video: {e}")

if __name__ == "__main__":
    try:
        hilo_sonido = threading.Thread(target=sensor_sonido)
        hilo_temperatura = threading.Thread(target=sensor_temperatura)
        hilo_video = threading.Thread(target=stream_with_gstreamer)

        hilo_sonido.start()
        hilo_temperatura.start()
        hilo_video.start()

        hilo_sonido.join()
        hilo_temperatura.join()
        hilo_video.join()
    except KeyboardInterrupt:
        print("Interrupcion detectada. Deteniendo...")
        stop_stream = True
    except Exception as e:
        print(f"Error general: {e}")
# Fin de código (remote)