#include "esp_camera.h" 
#include <WiFi.h>
#include <Arduino.h>

// ========== CONFIGURACIÓN DEL MODELO DE CÁMARA ==========
#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

// ========== CREDENCIALES DE RED WIFI ==========
const char* ssid = "Queti";
const char* password = "simi1234";

// ========== CONFIGURACIÓN DEL SENSOR ULTRASÓNICO ==========
const int trigPin = 16;         // TRIG del HC-SR04
const int echoPin = 15;         // ECHO del HC-SR04
const int DISTANCIA_LIMITE = 90; // Distancia en cm para detener

// Variables de medición
long duracion;
int distanciaCm;
bool programaDetenido = false;
bool mensajeDetenidoImpreso = false;

// Declaración de funciones externas
void startCameraServer();
void setupLedFlash(int pin);

// Función para medir la distancia con el HC-SR04
void medirDistancia() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duracion = pulseIn(echoPin, HIGH, 30000);  // Timeout de 30ms
  distanciaCm = (duracion == 0) ? 999 : duracion * 0.034 / 2;
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println("\nIniciando cámara y sensor HC-SR04...");

  // Configurar pines del HC-SR04
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  delay(100);

  // ================= CONFIGURACIÓN DE LA CÁMARA =================
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.grab_mode = CAMERA_GRAB_LATEST;

  if (psramFound()) {
    config.jpeg_quality = 10;
    config.fb_count = 2;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Error al iniciar la cámara: 0x%x\n", err);
    return;
  }

#if defined(LED_GPIO_NUM)
  setupLedFlash(LED_GPIO_NUM);
#endif

  // ================= CONEXIÓN A WIFI =================
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);
  Serial.print("Conectando a WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado");
  Serial.print("Dirección IP: http://");
  Serial.println(WiFi.localIP());

  // ================= INICIAR SERVIDOR DE CÁMARA =================
  startCameraServer();
  Serial.println("Cámara lista. Esperando detección de proximidad...");
}

void loop() {
  if (!programaDetenido) {
    medirDistancia();

    Serial.print("Distancia: ");
    Serial.print(distanciaCm);
    Serial.println(" cm");

    if (distanciaCm < DISTANCIA_LIMITE) {
      programaDetenido = true;
      Serial.println("¡Objeto detectado cerca!");
      Serial.print("Accede a la cámara en: http://");
      Serial.println(WiFi.localIP());
    }

    delay(500);
  } else {
    if (!mensajeDetenidoImpreso) {
      mensajeDetenidoImpreso = true;
      Serial.println("Programa detenido por proximidad.");
    }
    delay(1000);
  }
}
