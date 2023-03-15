/*
 * File: main.cpp
 * Project: D02_SD2_FA20
 * Author: Benjamin Blouin
 * Date: Fall 2020
 * 
 * Description: This source code sets up a deep sleep timer
 *              that runs a custom deep sleep wakeup stub.
 *              The stub is loaded into RTC(aka deep sleep) 
 *              fast memory. It has to be fast because it
 *              is code. Data can be kept in slow variables
 *              as seen in the file.
 * 
 * Citation: Heltec Design 
 * GitHub:https://github.com/HelTecAutomation/Heltec_ESP32
*/

#include "heltec.h"
#include "esp_sleep.h"
#include "../../Wire/src/Wire.h"
#include "esp32-hal-adc.h"

size_t number = 0;
//size_t state = 0;
unsigned int counter = 0;

#define uS_TO_S_FACTOR 1000000 //Conversion factor us to s
#define TIME_TO_SLEEP 20       //Duration ESP32 will sleep (in seconds) = 35.783 minutes
#define BAND 915E6             //LoRa US 915Mhz

RTC_DATA_ATTR size_t bootCount = 0; //Saved in slow ram

// Notice this is never called
void RTC_IRAM_ATTR esp_wake_deep_sleep(void)
{ //Runs from fast ram firmware
  esp_default_wake_deep_sleep();
  ++bootCount;
}

//Debug legacy
void print_wakeup_reason()
{
  esp_sleep_wakeup_cause_t wakeup_reason; //typdef constructor
  wakeup_reason = esp_sleep_get_wakeup_cause();
  switch (wakeup_reason)
  {
  case ESP_SLEEP_WAKEUP_EXT0:
    Serial.println("Wakeup caused by external signal using RTC_IO");
    break;
  case ESP_SLEEP_WAKEUP_EXT1:
    Serial.println("Wakeup caused by external signal using RTC_CNTL");
    break;
  case ESP_SLEEP_WAKEUP_TIMER:
    Serial.println("Wakeup caused by timer");
    break;
  case ESP_SLEEP_WAKEUP_TOUCHPAD:
    Serial.println("Wakeup caused by touchpad");
    break;
  case ESP_SLEEP_WAKEUP_ULP:
    Serial.println("Wakeup caused by ULP program");
    break;
  default:
    Serial.printf("Wakeup was not caused by deep sleep: %d\n", wakeup_reason);
    break;
  }
}

void sendAlarm()
{
  // send packet
  LoRa.beginPacket();
  LoRa.setTxPower(20, RF_PACONFIG_PASELECT_PABOOST);
  LoRa.print("ALARM");
  LoRa.endPacket();
}

void setup()
{
  Heltec.begin(false /*DisplayEnable Enable*/, true /*Heltec.LoRa Enable*/, true /*Serial Enable*/, true /*PABOOST Enable*/, BAND /*long BAND*/);
  Serial.printf("SERIAL ENTRY\n");
  Serial.printf("bootCount: %d\n", bootCount);

  if(bootCount==0){
      Serial.println("initial sleep");
      esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR); //Set timer
      esp_deep_sleep_start();
  }
  
  //for state control
  pinMode(GPIO_NUM_13, INPUT_PULLDOWN);
  // wakeup rpi
  //
  pinMode(GPIO_NUM_25, OUTPUT);
  digitalWrite(GPIO_NUM_25, HIGH);
  delay(100);
  digitalWrite(GPIO_NUM_25, LOW);

  // wait for rpi to finish
  //
  while (digitalRead(GPIO_NUM_13) == 0){}

  delay(2000);

  if (digitalRead(GPIO_NUM_13) == 1)
  {
    Serial.println("SEND ALARM");
    sendAlarm();
    while(true){}
  }
  
  else
  {
     //go to sleep
      Serial.println("going to sleep");
      esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR); //Set timer
      esp_deep_sleep_start();
  }

}

// Never Runs
void loop()
{
}
