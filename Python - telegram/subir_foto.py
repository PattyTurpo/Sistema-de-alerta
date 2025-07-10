import requests
import time
import datetime
import os
import cv2
import numpy as np

# 📁 Carpeta local
upload_folder = "uploads"
os.makedirs(upload_folder, exist_ok=True)

# 🧠 Clasificador de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# 🔐 Datos reales de Telegram
BOT_TOKEN = "7566014980:AAFHByjv_ipK-AQ64fcTrOhPFtKRm4mzvq0"
CHAT_ID = "7271105781"

# 🌐 URL del servidor PHP
SERVIDOR_URL = "http://192.168.56.1/upload.php"

# 📤 Subir imagen al servidor
def subir_archivo(ruta_local, servidor_url):
    with open(ruta_local, 'rb') as f:
        files = {'fileToUpload': f}
        response = requests.post(servidor_url, files=files)
    return response

# ✉ Enviar imagen a Telegram
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

# 📷 Capturar imagen desde la cámara de la PC
def capturar_pc():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ No se pudo acceder a la cámara.")
        return None

    ret, frame = cam.read()
    cam.release()

    if ret:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = f"{upload_folder}/foto_{timestamp}.jpg"
        cv2.imwrite(img_path, frame)
        return img_path
    else:
        print("❌ No se pudo capturar imagen.")
        return None

# 🤖 Detectar rostro y subir
def detectar_y_subir():
    img_path = capturar_pc()
    if img_path is None:
        return

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        response = subir_archivo(img_path, SERVIDOR_URL)
        if response.status_code == 200:
            enviar_a_telegram(img_path)
            print(f"📸 Imagen con rostro enviada: {img_path}")
        else:
            print("⚠ Error al subir imagen.")
    else:
        print("ℹ No se detectó rostro.")

# 🔁 Bucle principal
try:
    while True:
        detectar_y_subir()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n🛑 Programa finalizado.")
