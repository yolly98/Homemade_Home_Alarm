#ifndef MOVEMENT_SENSOR
#define MOVEMENT_SENSOR

#include "sensor_node_alarm.h"

void MovementSensor::init(){
  status = false;
  pinMode(MOVEMENT_SENSOR, INPUT);
  pinMode(EXT_LED, OUTPUT);
  pinMode(RELAY, OUTPUT);

  digitalWrite(RELAY, HIGH);
  digitalWrite(EXT_LED, LOW);
}

void MovementSensor::activateAlarm(){
  status = true;
  digitalWrite(RELAY, LOW);
  bool led_status = false;
  digitalWrite(EXT_LED, LOW);
  for(int i = 0; i < floor(ACTIVATION_DELAY / EXT_LED_BLINK_INTERVAL); i++){
    led_status = !led_status;
    if (led_status)
      digitalWrite(EXT_LED, HIGH);
    else
      digitalWrite(EXT_LED, LOW);
    delay(EXT_LED_BLINK_INTERVAL);
  }
  digitalWrite(EXT_LED, LOW);
}

void MovementSensor::deactivateAlarm(){
  status = false;
  digitalWrite(RELAY, HIGH);
  digitalWrite(EXT_LED, LOW);
}

// retirn true if detect a movement
bool MovementSensor::check(){
  if(!status) return false;

  if(digitalRead(MOVEMENT_SENSOR) == HIGH){
    // no movements detected
    digitalWrite(EXT_LED, HIGH);
    return true;
  }
  else{
    // movement detected
    digitalWrite(EXT_LED, LOW);
    return false;
  }
}

bool MovementSensor::getStatus(){
  return status;
}

#endif