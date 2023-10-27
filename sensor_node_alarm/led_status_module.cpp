#ifndef LED_STATUS_MODULE
#define LED_STATUS_MODULE

#include "sensor_node_alarm.h"

void LedStatusModule::init(){
  status = Colors::Off;
  pinMode(LEDR, OUTPUT);
  pinMode(LEDB, OUTPUT);
  pinMode(LEDG, OUTPUT);

  digitalWrite(LEDR, LOW);
  digitalWrite(LEDB, LOW);
  digitalWrite(LEDG, LOW);
}

void LedStatusModule::set(Colors color){
  status = color;
  switch (color){
    case Colors::Red:
      digitalWrite(LEDR, HIGH);
      digitalWrite(LEDB, LOW);
      digitalWrite(LEDG, LOW);
      break;
    case Colors::Blue:
      digitalWrite(LEDR, LOW);
      digitalWrite(LEDB, HIGH);
      digitalWrite(LEDG, LOW);
      break;
    case Colors::Green:
      digitalWrite(LEDR, LOW);
      digitalWrite(LEDB, LOW);
      digitalWrite(LEDG, HIGH);
      break;
    case Colors::White:
      digitalWrite(LEDR, HIGH);
      digitalWrite(LEDB, HIGH);
      digitalWrite(LEDG, HIGH);
      break;
    case Colors::Off:
      digitalWrite(LEDR, LOW);
      digitalWrite(LEDB, LOW);
      digitalWrite(LEDG, LOW);
      break; 
  }
}

Colors LedStatusModule::getStatus(){
  return status;
}


#endif