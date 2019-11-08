#include "ESP8266WiFi.h"
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>
#include <user_interface.h>
Adafruit_PCD8544 display = Adafruit_PCD8544(D4, D3, D2, D1, D0);
float instantMeasure = 0;
int h=0,m=0,s=0;
void setup() {
  //Debug purpose
  Serial.begin(9600);
  Serial.println("Started!");
  //Debug purpose
  setupDisplay();
}

void loop(){
  timer();
  voltageMeasure();
  //debug purpose
  Serial.println(instantMeasure);
  //debug purpose
  showOnDisplay();
  delay(100);
}

void voltageMeasure()
{
  instantMeasure = (analogRead(A0)*3.3/1023)-1.65;
}

void timer()
{
  if(s < 59)
    s++;
  else
  {
    s = 0;
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
}

void setupDisplay()
{
  display.begin();
  display.setContrast(48);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(BLACK);
}

void showOnDisplay()
{
  display.clearDisplay();

  display.setTextColor(BLACK,WHITE);
  
  display.drawRect(0, 0,  84, 48, 2);
  display.fillRect(0, 0,  84, 15, 2);
  display.fillRect(0, 33, 84, 48, 2);
  display.setCursor(10,20);
  display.setTextSize(1);
  display.print(instantMeasure);
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

  display.setCursor(20,38);
  display.print("Wifi Off!");
  display.display();
}
