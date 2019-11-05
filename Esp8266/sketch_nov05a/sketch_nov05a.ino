#include "ESP8266WiFi.h"

const char* ssid = "Elvis";
const char* password = "angaroth";
const char* passwordTrue = "angaroth1";

float leitura;

void setup() {
  int *count = new int(0);
  Serial.begin(9600);
  WiFi.begin(ssid,passwordTrue);
  while (WiFi.status() != WL_CONNECTED)
  {
    if(count[0] >= 9)
      break;
    delay(500);
    Serial.print("*");
    Serial.print(count[0]);
    count[0]++;
  }
  count = NULL;
  delete count;
  if(WiFi.status() == WL_CONNECTED)
  {
    Serial.print(" ");
    Serial.println("Conectado!");
    Serial.print("IP do 8266: ");
    Serial.println(WiFi.localIP());
  }
  else
  {
    Serial.print(" ");
    Serial.println("Não Conectado! O sistema conectará automaticamente assim que possível");
  }
}

void loop() {
  Serial.print(analogRead(A0));
  Serial.print("            ");
  leitura = (analogRead(A0)*3.3/1023);
  Serial.println(leitura);
  if(WiFi.status() != WL_CONNECTED){
    Serial.println("Tentando reconectar ao wi-fi!");
    WiFi.begin(ssid,password);
  }
  delay(1000);
}
