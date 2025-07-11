import requests
import datetime
import os
import cv2
import numpy as np

# 📁 Carpeta local
upload_folder = "uploads"
os.makedirs(upload_folder, exist_ok=True)

# 🧠 Clasificador de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# 🔐 Datos de Telegram
BOT_TOKEN = "7566014980:AAFHByjv_ipK-AQ64fcTrOhPFtKRm4mzvq0"
CHAT_ID = "7271105781"

# 🌐 URL de ESP32-CAM y servidor PHP
ESP32_CAM_URL = "http://192.168.121.7/capture"
SERVIDOR_URL = "http://localhost/upload.php"

# 📤 Subir imagen al servidor
def subir_archivo(ruta_local, servidor_url):
    with open(ruta_local, 'rb') as f:
        files = {'fileToUpload': f}
        response = requests.post(servidor_url, files=files)
    return response

# ✉ Enviar a Telegram
def enviar_a_telegram(imagen_path):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(imagen_path, 'rb') as photo:
            response = requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": photo})
        if response.status_code == 200:
            print("✅ Imagen enviada a Telegram.")
        else:
            print("❌ Telegram error:", response.text)
    except Exception as e:
        print("❌ Conexión Telegram fallida:", e)

# 🔁 Detección continua desde ESP32-CAM
def detectar_desde_esp32():
    rostro_detectado_anterior = False

    try:
        while True:
            try:
                # Obtener imagen del ESP32-CAM
                resp = requests.get(ESP32_CAM_URL, timeout=2)
                if resp.status_code != 200:
                    continue
                img_array = np.frombuffer(resp.content, np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if frame is None:
                    continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                if len(faces) > 0:
                    if not rostro_detectado_anterior:
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        img_path = f"{upload_folder}/rostro_{timestamp}.jpg"
                        cv2.imwrite(img_path, frame)

                        response = subir_archivo(img_path, SERVIDOR_URL)
                        if response.status_code == 200:
                            enviar_a_telegram(img_path)
                            print(f"📸 Rostro detectado y enviado: {img_path}")
                        else:
                            print("⚠ Error al subir la imagen.")

                        rostro_detectado_anterior = True
                else:
                    rostro_detectado_anterior = False

            except requests.exceptions.RequestException:
                print("⚠ ESP32-CAM no responde. Reintentando...")

    except KeyboardInterrupt:
        print("\n🛑 Programa finalizado.")

# ▶ Iniciar
detectar_desde_esp32()
