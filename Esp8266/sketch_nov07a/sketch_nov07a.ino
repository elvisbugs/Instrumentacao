#include "ESP8266WiFi.h"
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>
#include <user_interface.h>
#include <math.h>

// Nokia 5110 LCD module connections (CLK, DIN, D/C, CS, RST)
Adafruit_PCD8544 display = Adafruit_PCD8544(D4, D3, D2, D1, D0);
double instantMeasure = 0;
double Vrms = 0;
int h = 0,m = 0,s = 0;
double sAdjusted = 0;

void setup() {
  Serial.begin(9600);
  setupDisplay();
}

void loop(){
  timer();
  voltageMeasure();
  char test[10];
  sprintf(test, "%.5f",Vrms);
  Serial.println(test);
  showOnDisplay();
  Vrms = 0;
}

void voltageMeasure(){
  double tst = 0;
  for(int i=0; i < 1500; i++)
  {
    instantMeasure = (analogRead(A0)*3.3/1023)-1.65;
    tst = sqrt(pow(instantMeasure,2)); 
    if(tst > Vrms)
      Vrms = tst;  
    delayMicroseconds(666);
  }
  double pow1 = pow(10,-11);
  double mul = 1.147314*pow1;
  double dem = pow(Vrms/(mul),0.6645585) + 1;
  //double dem = 1 + pow((Vrms/1.147314*pow(10,-11)),0.6645585); 
  Vrms = 92.6621 + (-100164800-92.6621) / dem;
  //Vrms = Vrms /100;
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
  s = round(sAdjusted);
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

  display.setCursor(20,38);
  display.print("Wifi Off!");
  display.display();
}
