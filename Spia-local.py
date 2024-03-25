import os
import time
import pyfiglet # pip install -r requirements.txt
import keyboard # Python.exe Monitoreo-remoto.py
import numpy as np  # Importar numpy para funciones relacionadas con matrices
import cv2  # Importar OpenCV para procesamiento de imágenes y videos
import pyautogui  # Importar pyautogui para captura de pantalla
import sounddevice as sd  # Importar sounddevice para grabación de audio
import soundfile as sf  # Importar soundfile para escritura de archivos de audio
from colorama import Fore, Style  # Importar clases Fore y Style de colorama

# Resto del código...

def grabar_video(directory, duration, filename):
    start_time = time.time()
    end_time = start_time + duration
    screen_width, screen_height = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(os.path.join(directory, filename), fourcc, 20.0, (screen_width, screen_height))

    while time.time() < end_time:
        # Capturar la pantalla
        screenshot = pyautogui.screenshot()

        # Convertir la captura de pantalla a un array numpy y luego a un array OpenCV
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Escribir el frame en el video
        out.write(frame)

    out.release()

def capturar_pantalla(directory):
    # Crear la carpeta "monitoreo" dentro de la carpeta de imágenes
    monitoreo_directory = os.path.join(directory, "monitoreo")
    if not os.path.exists(monitoreo_directory):
        os.makedirs(monitoreo_directory)

    # Contador para el nombre de las capturas de pantalla
    counter = 1

    while True:
        try:
            # Capturar la pantalla
            screenshot = pyautogui.screenshot()

            # Guardar la captura en la carpeta de monitoreo
            screenshot.save(os.path.join(monitoreo_directory, f"screenshot_{counter}.png"))

            print(f"Captura {counter} guardada.")

            # Esperar 5 segundos antes de la próxima captura
            time.sleep(5)

            # Incrementar el contador
            counter += 1

        except KeyboardInterrupt:
            print("Captura de pantalla detenida por el usuario.")
            break
        except Exception as e:
            print(f"Error al capturar pantalla: {e}")

def grabar_audio(directory, duration, filename):
    sample_rate = 44100  # Frecuencia de muestreo
    channels = 2         # Canales de audio (estéreo)

    # Calcular el número de frames a grabar
    frames_to_record = int(duration * sample_rate)

    # Inicializar un array para almacenar los frames grabados
    recorded_frames = np.empty((frames_to_record, 2), dtype=np.float32)

    print("Grabando audio...")

    # Grabar audio utilizando sounddevice
    recorded_frames = sd.rec(frames_to_record, samplerate=sample_rate, channels=channels, dtype=np.float32)

    # Esperar hasta que la grabación termine
    sd.wait()

    # Guardar el archivo de audio en formato WAV
    sf.write(os.path.join(directory, filename), recorded_frames, sample_rate)
    print(f'Audio {filename} guardado correctamente.')

def grabar_desde_webcam(directory, duration):
    # Crear la carpeta "webcam" dentro de la carpeta de videos
    webcam_directory = os.path.join(directory, "webcam")
    if not os.path.exists(webcam_directory):
        os.makedirs(webcam_directory)

    # Nombre del archivo de video
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(webcam_directory, f"webcam_{timestamp}.avi")

    # Configurar la captura de video desde la webcam
    cap = cv2.VideoCapture(0)

    # Configurar el codec y el objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = time.time()
    end_time = start_time + duration

    # Iniciar la grabación desde la webcam
    while time.time() < end_time:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break

    # Liberar recursos
    cap.release()
    out.release()

    print(f'Video de la webcam {filename} guardado correctamente.')

def guardar_pulsaciones(directory):
    # Crear la carpeta "pulsaciones" dentro de la carpeta de documentos
    pulsaciones_directory = os.path.join(directory, "pulsaciones")
    if not os.path.exists(pulsaciones_directory):
        os.makedirs(pulsaciones_directory)

    # Nombre del archivo para guardar las pulsaciones
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(pulsaciones_directory, f"pulsaciones_{timestamp}.txt")

    print("Guardando pulsaciones de teclado... (Presione 'Esc' para detener)")

    # Iniciar la grabación de pulsaciones de teclado
    events = []
    while True:
        event = keyboard.read_event()
        events.append(event)
        if event.name == "esc":
            break

    # Abrir el archivo en modo escritura
    with open(filename, 'w') as file:
        for event in events:
            # Convertir el evento a una cadena y escribirlo en el archivo
            event_str = str(event)
            file.write(event_str + '\n')

    print(f'Pulsaciones guardadas en {filename}.')

def mostrar_menu():
    ascii_banner = pyfiglet.figlet_format("4ZESINO")
    ascii_banner = (Fore.BLUE + ascii_banner + Style.RESET_ALL)
    print(ascii_banner)
    print(Fore.CYAN + "1. Capturar pantalla")
    print(Fore.CYAN + "2. Grabar video")
    print(Fore.CYAN + "3. Grabar audio")
    print(Fore.CYAN + "4. Grabar desde webcam")
    print(Fore.CYAN + "5. Guardar pulsaciones de teclado")
    print(Fore.CYAN + "6. Salir del programa" + Style.RESET_ALL)

def main():
    while True:
        mostrar_menu()
        opcion = input(Fore.RED + "Seleccione una opción: " + Style.RESET_ALL)

        if opcion == "1":
            # Directorio donde se guardarán las capturas de pantalla
            directory = os.path.join(os.path.expanduser("~"), "Pictures")

            # Llamar a la función para capturar pantalla cada 5 segundos
            capturar_pantalla(directory)
        elif opcion == "2":
            # Directorio donde se guardarán los videos
            directory = os.path.join(os.path.expanduser("~"), "Videos")

            # Crear la carpeta si no existe
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Nombre del archivo de video
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"video_{timestamp}.avi"

            # Duración del video en segundos (10 minutos)
            duration = 600

            # Grabar el video
            grabar_video(directory, duration, filename)

            print(f'Video {filename} guardado correctamente.')
        elif opcion == "3":
            # Directorio donde se guardarán los archivos de audio
            directory = os.path.join(os.path.expanduser("~"), "Music")

            # Crear la carpeta si no existe
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Nombre del archivo de audio
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"audio_{timestamp}.wav"

            # Duración de la grabación en segundos (10 minutos)
            duration = 600

            # Grabar audio
            grabar_audio(directory, duration, filename)
        elif opcion == "4":
            # Directorio donde se guardarán los videos
            directory = os.path.join(os.path.expanduser("~"), "Videos")

            # Duración del video en segundos (10 minutos)
            duration = 600

            # Grabar desde la webcam
            grabar_desde_webcam(directory, duration)
        elif opcion == "5":
            # Directorio donde se guardarán las pulsaciones de teclado
            directory = os.path.join(os.path.expanduser("~"), "Documents")

            # Llamar a la función para guardar pulsaciones de teclado
            guardar_pulsaciones(directory)
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()

