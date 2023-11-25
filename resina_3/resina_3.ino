#include <LiquidCrystal_I2C.h>
#include <Wire.h>


int buz = 4 ;

int piu=11;
int meno=12;
int ok=2;
 int prog=3;

int mix=9;
int base=10;

//SDA A4 - SCL A5

int stato=0;
 int set=0;

LiquidCrystal_I2C lcd(0x27,16,2);

void setup()
{
  pinMode(buz,OUTPUT);
  pinMode(piu,INPUT_PULLUP);
  pinMode(meno,INPUT_PULLUP);
  pinMode(ok,INPUT_PULLUP);
   pinMode(prog,INPUT_PULLUP);
  Serial.begin(9600);
 lcd.init();
lcd.backlight();
  
}

void loop()
{
  if(digitalRead(prog))
{
  stato=0;
}
if(!digitalRead(prog))
{
  stato=1;
}
  
  
  if(!digitalRead(piu))
{
  set=set+1;
  delay(200);
}
 
if(!digitalRead(meno))
{
  set=set-1;
  delay(200);
} 

if(set<=1)
{
  set=1;
} 
  
  
   char buf[3]; // buffer per contenere la stringa formattata
  sprintf(buf, "%02d", set);
  
  switch(stato)
  {
  
 case 0:
    lcd.home();
    lcd.print("Lavagio");
    lcd.setCursor(0,1);
    lcd.print("Timer:");
   
     lcd.setCursor(7,1);
    lcd.print(buf);
    
 if(!digitalRead(ok))
{
  Serial.println("stonks");

}
    
    
    
    break;
    
 case 1:
      lcd.home();
    lcd.print("Cottura");
     lcd.setCursor(0,1);
    lcd.print("Timer:");
     lcd.setCursor(7,1);
    lcd.print(buf);
    
     if(!digitalRead(ok))
{
  digitalWrite(base,HIGH);
  
  if(timer(set))
     {
       digitalWrite(base,LOW);
     }
}
    
    
    break; 
     
  }
  
  
} // fine loop



int timer (unsigned long t1)
{
   t1=t1*1000;
  static unsigned long tx, dt;
  int ret=0;
  dt=millis(); - tx;
  
  if(dt>=t1)
  {
    tx=millis();
    ret=1;   
  }
  
  return ret;
  
}
