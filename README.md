# Proyecto de Monitoreo y Streaming con Raspberry Pi

Este proyecto permite monitorear sensores de sonido y temperatura, así como realizar streaming de video utilizando una Raspberry Pi y AWS Kinesis Video Streams. Incluye el envío de notificaciones basadas en la detección de eventos anormales.

## Funcionalidades

- Sensor de sonido: Detección de picos de sonido (llanto, ruidos elevados) con alertas enviadas a un servidor.
- Sensor de temperatura: Detección de temperaturas fuera de rango con notificaciones periódicas.
- Streaming de video: Envío de video en tiempo real utilizando GStreamer y AWS Kinesis.

## Requisitos

- Raspberry Pi con cámara compatible (NoIR V2 o similar).
- Sensores:
- Sensor de sonido compatible con I2C (ADS1115).
- Sensor de temperatura (W1ThermSensor).
- Conexión a internet.
- Cuenta en AWS con acceso a Kinesis Video Streams.

## Instalación

1. Clonar el repositorio:
	```
	git clone <URL_DEL_REPOSITORIO>
	cd <NOMBRE_DEL_REPOSITORIO>
	```
2. Configurar entorno virtual (opcional):
	```
	python3 -m venv venv
	source venv/bin/activate
	```
3. Instalar dependencias:
	```
	pip install -r requirements.txt
	```
### Configurar variables de entorno:
Crear un archivo .env con las siguientes variables:
```
EMAIL=tu_correo@example.com
SOUND_ENDPOINT=https://tu-endpoint-sound.com
TEMP_ENDPOINT=https://tu-endpoint-temp.com
AWS_ACCESS_KEY_ID=TU_AWS_KEY
AWS_SECRET_ACCESS_KEY=TU_AWS_SECRET
AWS_REGION=us-east-1
STREAM_NAME=nombre_stream
```


## Uso

- Ejecutar el monitoreo

		Para iniciar los sensores y el streaming:
		```
		python3 main.py
		```
- Interrupción manual
		Presiona Ctrl + C para detener la ejecución del programa.

##Seguridad
Manejo de credenciales: Las credenciales AWS y los endpoints están almacenados en variables de entorno y no deben subirse al repositorio.
Exclusión de archivos sensibles: Asegúrate de que .env está listado en el archivo .gitignore.

## Dependencias

- requests
- adafruit-circuitpython-ads1x15
- w1thermsensor
- python-dotenv
- busio
- requests