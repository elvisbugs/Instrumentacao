#include <ESP8266WiFi.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>
#include <user_interface.h>
#include <PubSubClient.h>
#include <math.h>
const String HOSTNAME  = "DeviceESP8266"; //NOME DO DEVICE, deverá ter um nome unico.
const char * sub_topic = "MNPS"; //Topico onde o Device subscreve.
const char * pub_topic = "Configs"; //Topico onde o Device publica.

//PODE SER CONFIGURADO POR SERIAL
String ssid = "Elvis";
String password = "angaroth";
String MQTT_SERVER = "192.168.0.103"; //IP ou DNS do Broker MQTT

// Nokia 5110 LCD module connections (CLK, DIN, D/C, CS, RST)
Adafruit_PCD8544 display = Adafruit_PCD8544(D4, D3, D2, D1, D0);

double instantMeasure = 0;

double Vrms = 0;
int h = 0,m = 0,s = 0;
double sAdjusted = 0;

String dataReceveid;
int timeWifiOff = 0;
String wifiState = "WiFi Off!";

String mqttMsg;

WiFiClient wclient;
PubSubClient client(MQTT_SERVER.c_str(), 1883, wclient);

void setup() {
  Serial.begin(9600);
  setupDisplay();
  setupWifi();
  client.setCallback(mqtt_callback);
}

void checkMqttConnection() {
  if (!client.connected()) {
    client.setServer(MQTT_SERVER.c_str(), 1883);
    if (client.connect(HOSTNAME.c_str())) {
      client.subscribe(sub_topic);
    }
  }
  else{
    client.loop();
    char data[20];
    sprintf(data,"%f",Vrms);
    client.publish(sub_topic, data);
  }
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) 
{
    String msg = "";
 
    for(int i = 0; i < length; i++) 
    {
       msg += (char)payload[i];
    }
    mqttMsg = msg;
}

void setupWifi(){
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid.c_str(),password.c_str());
  int count = 0;
  while (WiFi.status() != WL_CONNECTED) 
  {
     delay(500);
     if(count > 20){
        wifiState="WiFi Off!";
        return;
     }
     count++;
  }
  wifiState="WiFi On!";
}

void reconectWifi(){  
  if(WiFi.status() == WL_CONNECTED)
    return;

  if(!(WiFi.status() == WL_CONNECTED))
  {
    wifiState="WiFi Off!";
    if(timeWifiOff <=50)
    {
      timeWifiOff++;
      return;
    }
    
    else if(timeWifiOff > 50){
      timeWifiOff = 0;
      int count = 0;
      
      WiFi.mode(WIFI_AP_STA);
      WiFi.begin(ssid.c_str(),password.c_str());
      while (WiFi.status() != WL_CONNECTED) 
      {
        delay(1000);
        timer();
        showOnDisplay();
        if(count % 3 == 0){
          wifiState="Conecting.";
        }
        else{
          wifiState+=".";
        }
        if(count > 5)
            return;
        count++;
      }
      wifiState="WiFi On!";
    }
  }
}

void voltageMeasure(){
  Vrms = 0;
  for(int i=0; i < 1500; i++)
  {
    instantMeasure = (analogRead(A0)*3.3/1023)-1.65;
    instantMeasure = sqrt(pow(instantMeasure,2)); 
    if(instantMeasure > Vrms)
      Vrms = instantMeasure;  
    delayMicroseconds(500);
  }
  Vrms = 15.812*log10(Vrms) + 91.981;
}

void timer(){
  if(sAdjusted < 59)
    sAdjusted += 1,0205450734;
  else
  {
    sAdjusted = 0;
    if(m < 59)
      m++;
    else
    {
      m = 0;
      if(h < 23)
        h++;
      else
        h = 0;
    }
  }
  s = (int)sAdjusted;
}

void setupDisplay(){
  display.begin();
  display.setContrast(48);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(BLACK);
}

void showOnDisplay(){
  display.clearDisplay();

  display.setTextColor(BLACK,WHITE);
  
  display.drawRect(0, 0,  84, 48, 2);
  display.fillRect(0, 0,  84, 15, 2);
  display.fillRect(0, 33, 84, 48, 2);
  display.setCursor(10,20);
  display.setTextSize(1);
  display.print(Vrms);
  display.print(" dB(A)");
  
  display.setTextColor(WHITE,BLACK);
  display.setCursor(20,4);
  if(h < 10)
    display.print("0");
    
  display.print(h);  
  display.print(":");
  
  if(m < 10)
    display.print("0");
  
  display.print(m);
  display.print(":");

  if(s < 10)
    display.print("0");
  display.print(s);

  if(wifiState == "WiFi On!" || wifiState == "WiFi Off!")
    display.setCursor(20,38);
  else
    display.setCursor(10,38);
    
  display.print(wifiState);
  display.display();
}

void loop(){
  timer();
  voltageMeasure();
  showOnDisplay();
  reconectWifi();
  if(WiFi.status() == WL_CONNECTED)
    checkMqttConnection();
}
