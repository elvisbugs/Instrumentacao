#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>
#include <user_interface.h>
#include <PubSubClient.h>
#include <math.h>
WiFiUDP udp;
//PODE SER CONFIGURADO POR SERIAL
String ssid = "Elvis";
String password = "angaroth";
String ip = "192.168.1.101"; //IP ou DNS do Broker MQTT

// Nokia 5110 LCD module connections (CLK, DIN, D/C, CS, RST)
Adafruit_PCD8544 display = Adafruit_PCD8544(D4, D3, D2, D1, D0);

double dB = 0;
int h = 0,m = 0,s = 0;
double sAdjusted = 0;

double maxVal = 0;
double instantMeasure = 0;
double y = 0;

int timeWifiOff = 0;
String wifiState = "WiFi Off!";

void setup() {
  setupDisplay();
  setupWifi();
  Serial.begin(9600);
}

void setupWifi(){
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
  Serial.begin(9600);
  Serial.println(WiFi.localIP());
}

void reconectWifi(){  
  if(WiFi.status() == WL_CONNECTED)
  {
                    //ip, porta udp para enviar
    udp.beginPacket(ip.c_str(), 4242);
    udp.print(dB);//adiciona o dado ao pacote
    udp.endPacket();//envia
    return;
  }

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
  maxVal = 0;
  instantMeasure = 0;
  for(int i=0; i < 1500; i++)
  {
    instantMeasure = (analogRead(A0)*3.3/1023)-1.68;
    instantMeasure = sqrt(pow(instantMeasure,2)); 
    if(instantMeasure > maxVal)
      maxVal = instantMeasure;  
    delayMicroseconds(500);
  }
  y = ((13.904*log(maxVal)) + 92.459);
  if(maxVal <= 0.0361){
    maxVal = 0.0361;
  }
  if(maxVal >= 1.1100){
    maxVal = 1.1100;
  }
  if(maxVal <= 0.0490){
    dB = y - ((-0.45*maxVal + 0.081777)/0.0129);
  }
  else if(maxVal <= 0.0619){
    dB = y - ((-0.66*maxVal + 0.055926)/0.0096);
  }
  else if(maxVal <= 0.0748){
    dB = y - ((-1.79*maxVal + 0.107108)/0.0096);
  }
  else if(maxVal <= 0.1232){
    dB = y - ((-0.29*maxVal - 0.104664)/0.0322);
  }
  else if(maxVal <= 0.2587){
    dB = y - ((1.72*maxVal - 0.681156)/0.00968);
  }
  else if(maxVal <= 0.5490){
    dB = y - ((1.72*maxVal - 0.997564)/0.1903);
  }
  else{
    dB = y - ((1.25*maxVal - 0.151377)/0.2803);
  }
}

void timer(){
  if(sAdjusted < 59)
    sAdjusted += 1.0205450734;
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
  display.print(dB);
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
}
