#include<EEPROM.h>
#include<LiquidCrystal.h>


#include <Wire.h>

#include <Adafruit_Sensor.h> 

#include <Adafruit_ADXL345_U.h>

Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified();

//#include <Keypad.h>
LiquidCrystal lcd(13,12,8,9,10,11);

int RELAY=3;
int Buzzer=4;
int flag;

char ch;


char Start_buff[70]; 

int a=0,b=0,c=0,d=0;
void setup()
{


    pinMode(RELAY, OUTPUT);
    pinMode(Buzzer, OUTPUT);

    digitalWrite(RELAY,LOW);
    digitalWrite(Buzzer,LOW);
 
    Serial.begin(9600);
    lcd.begin(16,2);  
    lcd.clear();
    lcd.print("VEHICLE SAFETY");
    lcd.setCursor(0,1);
    lcd.print("AUTHENTICATION");
    delay(2000);
  
    if(!accel.begin())

   {

      Serial.println("No valid sensor found");

      while(1);

   }

}
 
void loop()
{
  START();
}

void START()
{
  lcd.clear();
  lcd.print("Waiting For Face");
  lcd.setCursor(0,1);
  lcd.print(" Authenticatin");
   while(1)
   {
     SerialEvent();
   }

}
void SerialEvent()
{
    if(Serial.available()>0)
    {
        ch=Serial.read();
        if(ch=='A')
        {
          lcd.clear();
          lcd.print("Face Matched");
          delay(2000);
          SENSOR_CHECK();
        }
        if(ch=='B')
        {
          lcd.clear();
          lcd.print("Face Not Matched");
          lcd.setCursor(0,1);
          lcd.print("Waiting.....");
          delay(2000);
    
        }
        if(ch=='C')
        {
          lcd.clear();
          lcd.print("Owner Given");
          lcd.setCursor(0,1);
          lcd.print("Permission.....");
          delay(2000);
          SENSOR_CHECK();
        }
        if(ch=='D')
        {
          lcd.clear();
          lcd.print("Owner Not Given");
          lcd.setCursor(0,1);
          lcd.print("Permission.....");
          delay(2000);
          //SENSOR_CHECK();
        }
//        if(result=='C')
//        {
//          lcd.clear();
//          lcd.print("FACE3 MATCHED");
//          delay(2000);
//         SENSOR_CHECK();
//        }
//        if(result=='D')
//        {
//          lcd.clear();
//          lcd.print("FACE4 MATCHED");
//          delay(2000);
//          SENSOR_CHECK();
//        
//        }
       
    }
} 

void SENSOR_CHECK()
{
  Serial.println("MOVING..");
  while(1)
  {
    
       IGNITION_ON();
       ACCIDENT();      
 
  }


}
void ACCIDENT()
{
    sensors_event_t event; 

   accel.getEvent(&event);

  float X_val=event.acceleration.x;

  float Y_val=event.acceleration.y;

   lcd.clear();
    lcd.print("X:");
    lcd.print(X_val);
    lcd.setCursor(0,1);
       lcd.print("Y:");
    lcd.print(Y_val);
    delay(1000);

//   Serial.print("X: "); Serial.print(event.acceleration.x); Serial.print("  ");
//
//   Serial.print("Y: "); Serial.print(event.acceleration.y); Serial.print("  ");
//
//   Serial.print("Z: "); Serial.print(event.acceleration.z); Serial.print("  ");
//
//   Serial.println("m/s^2 ");

  // delay(500);

   if((X_val<-7.50)||(X_val>7.5))
   {
    Serial.println("$ACCIDENT OCCURS#");
    lcd.clear();
    lcd.print("ACCIDENT OCCURS");
    digitalWrite(Buzzer,HIGH);
    delay(1000);
    digitalWrite(Buzzer,LOW);
    IGNITION_OFF();
    while(1);
   }
    if((Y_val<-7.50)||(Y_val>7.5))
   {
    Serial.println("$ACCIDENT OCCURS#");
    lcd.clear();
    lcd.print("ACCIDENT OCCURS");
     digitalWrite(Buzzer,HIGH);
    delay(1000);
    digitalWrite(Buzzer,LOW);
    IGNITION_OFF();
    while(1);
   }

} 

void IGNITION_ON()
{
    lcd.clear();
    lcd.print("IGNITION_ON");
    delay(1000);
    digitalWrite(RELAY,HIGH);
    delay(500);

}
void IGNITION_OFF()
{
//    lcd.clear();
//    lcd.print("IGNITION_OFF");
    digitalWrite(RELAY,LOW);
    delay(500);


}

char Serial_read(void)
{
      char ch;
      while(Serial.available() == 0);
      ch = Serial.read();
      return ch;
}

void Waiting()
{
  Serial.begin(9600);
   while(1)
  {
    if (Serial.available() > 0)
      {
        
          while(Serial_read()!='*');
        int  i=0;
          while((ch=Serial_read())!='#')
          {
            Start_buff[i] = ch;
             i++;
          }  
          Start_buff[i]='\0';
       }
     //  Serial.println(Start_buff);
    if(strcmp(Start_buff,"1234")==0)
    {
     
      Serial.begin(9600);
     Serial.println("Access Granted...");
    
      delay(2000);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Access");
      lcd.setCursor(0, 1);
      lcd.print("Granted.");
      digitalWrite(RELAY,HIGH);
           delay(1000);
      SENSOR_CHECK();
    
    }
   
  }
}
