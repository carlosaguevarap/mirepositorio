#include <SD.h> 
#include <SPI.h> 
#include <DHT.h> 
#include <TimeLib.h> 
#define DHTPIN 2 
#define DHTTYPE DHT22 

DHT dht(DHTPIN, DHTTYPE); 
int LDR=A0; 
int CS_pin=10; 
File sd_file; 

void setup() { 
  Serial.begin(9600); 
  setTime(19,26,50,29,05,2018); 
  pinMode(CS_pin, OUTPUT); 
  dht.begin(); 
  //SDCard Initialization 
  if (SD.begin()) { 
    Serial.print("SDCard is initialized. Ready to go"); 
  } 
  else { 
    Serial.println("Failed"); 
    return; 
  } 
  sd_file = SD.open("data.txt", FILE_WRITE);
  if (sd_file) { 
    Serial.print("Date"); 
    Serial.print(","); 
    Serial.print("Time"); 
    Serial.print(","); 
    Serial.print("Humidity %"); 
    Serial.print(","); 
    Serial.print("Temperature °C"); 
    Serial.print(","); 
    Serial.println("LDR"); 
    sd_file.print("Date"); 
    sd_file.print(","); 
    sd_file.print("Time"); 
    sd_file.print(","); 
    sd_file.print("Humidity"); 
    sd_file.print(","); 
    sd_file.print("Temperature °C"); 
    sd_file.print(","); 
    sd_file.println("LDR"); 
   } 
  sd_file.close(); //closing the file 
} 

void loop() { 
    time_t t=now(); 
    sd_file = SD.open("data.txt", FILE_WRITE); 
    if(sd_file) { 
      senddata(); 
    } 
    //if the file didn't open, print an error: 
    else { 
      Serial.println("error opening file"); 
    } 
    float h=dht.readHumidity();
    float te=dht.readTemperature(); 
    float l=analogRead(LDR); 
    Serial.print(day(t)); 
    Serial.print(+ "/"); 
    Serial.print(month(t)); 
    Serial.print(+ "/"); 
    Serial.print(year(t)); 
    Serial.print(","); 
    Serial.print(hour(t)); 
    Serial.print(+ ":"); 
    Serial.print(minute(t)); 
    Serial.print(+ ":"); 
    Serial.print(second(t)), 
    Serial.print(","); 
    Serial.print(h); 
    Serial.print(",    "); 
    Serial.print(te); 
    Serial.print(",       "); 
    Serial.println(l); 
}

void senddata() { 
    float h=dht.readHumidity(); 
    float t=dht.readTemperature(); 
    float l=analogRead(LDR); 
    sd_file.print(day(t)); 
    sd_file.print(+ "/"); 
    sd_file.print(month(t)); 
    sd_file.print(+ "/"); 
    sd_file.print(year(t)); 
    sd_file.print(","); 
    sd_file.print(hour(t)); 
    sd_file.print(":"); 
    sd_file.print(minute(t)); 
    sd_file.print(":"); 
    sd_file.print(second(t)); 
    sd_file.print(",  "); 
    sd_file.print(h); 
    sd_file.print(",    "); 
    sd_file.print(t); 
    sd_file.print(",      "); 
    sd_file.println(l); 
    sd_file.flush(); //saving the file 
    delay(5000);
  sd_file.close(); //closing the file 
} 
