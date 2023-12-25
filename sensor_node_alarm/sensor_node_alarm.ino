#ifndef SENSOR_NODE_ALARM
#define SENSOR_NODE_ALARM

#include "sensor_node_alarm.h"

uint8_t MODE = SOLO_MODE;

LedStatusModule ledStatusModule;
CommunicationModule communicationModule;
MovementSensor movementSensor;
bool movementDetected = false;
unsigned long keep_alive_timer = NULL;

void setup(){
  
  // MODULES INIZIALIZATION
  pinMode(RESET, OUTPUT);
  digitalWrite(RESET, LOW);

  Serial.begin(9600);
  
  ledStatusModule.init();
  movementSensor.init();
  ledStatusModule.set(Colors::White);
  communicationModule.initializeUDP();

  delay(1000);

  char packet[PACKET_SIZE];
  sprintf(packet, "/%s/%s/INIT",ROOM, SENSOR_ID);

  // INITIALIZATION PROTOCOL
  // The sensor node attempts to contact the server to register itself in the network.
  // If it doesn't receve any response, it will work in SOLO_MODE, otherwise in NET_MODE
  int max_attempts = COMMUNICATION_ATTEMPTS;
  while(max_attempts > 0){
    communicationModule.sendPacket(packet, (IPAddress)SERVER_IP, (uint16_t)SERVER_PORT);
    delay(SENDING_DELAY);

    IPAddress ip;
    uint16_t port;
    char receivedPacket[PACKET_SIZE];
    if (communicationModule.receivePacket(receivedPacket, &ip, &port)){

      if(strcmp(receivedPacket, "ACK") == 0){
        MODE = NET_MODE;
        ledStatusModule.set(Colors::Blue);
        keep_alive_timer = millis();
        break;
      } else{
        ledStatusModule.set(Colors::Red);
        while(true){delay(1000);};
      }
    }
    max_attempts--;
  }
  if(MODE == SOLO_MODE){
    // In SOLO_MODE the alarm is always activated
    ledStatusModule.set(Colors::Green);
    movementSensor.activateAlarm();
  }

}

void loop(){

  if(MODE == SOLO_MODE){
    movementDetected = movementSensor.check();
  }
  else if(MODE == NET_MODE){

    // Contact Server every KEEP_ALIVE_TIMER
    if(millis() - keep_alive_timer > KEEP_ALIVE_TIMER){

      char packet[PACKET_SIZE];
      
      if(movementSensor.getStatus()){
          sprintf(packet, "/%s/%s/ON",ROOM, SENSOR_ID);
          communicationModule.sendPacket(packet, SERVER_IP, (uint16_t)SERVER_PORT);
          delay(SENDING_DELAY);
      }
      else{
        char packet[PACKET_SIZE];
        sprintf(packet, "/%s/%s/OFF",ROOM, SENSOR_ID);
        communicationModule.sendPacket(packet, SERVER_IP, (uint16_t)SERVER_PORT);
        delay(SENDING_DELAY);
      }
      keep_alive_timer = millis();
    }

    // Check if there is a new message from the server
    IPAddress ip;
    uint16_t port;
    char receivedPacket[PACKET_SIZE];

    if (communicationModule.receivePacket(receivedPacket, &ip, &port)){

      char packet[PACKET_SIZE];

      if(strcmp(receivedPacket, "RESET") == 0){
        sprintf(packet, "/%s/%s/RESET",ROOM, SENSOR_ID);
        communicationModule.sendPacket(packet, ip, (uint16_t)SERVER_PORT);
        delay(SENDING_DELAY);
        digitalWrite(RESET, HIGH);
      }
      else if(strcmp(receivedPacket, "ON") == 0){
        sprintf(packet, "/%s/%s/ON",ROOM, SENSOR_ID);
        communicationModule.sendPacket(packet, ip, (uint16_t)SERVER_PORT);
        delay(SENDING_DELAY);
        movementSensor.activateAlarm();
      }
      else if(strcmp(receivedPacket, "OFF") == 0){
        sprintf(packet, "/%s/%s/OFF",ROOM, SENSOR_ID);
        communicationModule.sendPacket(packet, ip, (uint16_t)SERVER_PORT);
        delay(SENDING_DELAY);
        movementSensor.deactivateAlarm();
      }
      else if(strcmp(receivedPacket, "STATUS") == 0){
        if(movementSensor.getStatus()){
          sprintf(packet, "/%s/%s/ON",ROOM, SENSOR_ID);
          communicationModule.sendPacket(packet, ip, (uint16_t)SERVER_PORT);
          delay(SENDING_DELAY);
        }
        else{
          char packet[PACKET_SIZE];
          sprintf(packet, "/%s/%s/OFF",ROOM, SENSOR_ID);
          communicationModule.sendPacket(packet, ip, (uint16_t)SERVER_PORT);
          delay(SENDING_DELAY);
        }
      }

    }

    // If the alarm is activated and a movement is detected the sensor node alert the server
    bool tmp = movementSensor.check();
    if(tmp != movementDetected){

      char packet[PACKET_SIZE];

      if(tmp)
        sprintf(packet, "/%s/%s/DETECTED",ROOM, SENSOR_ID);
      else
        sprintf(packet, "/%s/%s/FREE",ROOM, SENSOR_ID);

      int max_attempts = COMMUNICATION_ATTEMPTS;
      while(max_attempts > 0){
        communicationModule.sendPacket(packet, (IPAddress)SERVER_IP, (uint16_t)SERVER_PORT);
        delay(SENDING_DELAY);

        IPAddress ip;
        uint16_t port;
        char receivedPacket[PACKET_SIZE];
        if (communicationModule.receivePacket(receivedPacket, &ip, &port)){

          if(strcmp(receivedPacket, "ACK") == 0)
            break;
        }
        max_attempts--;
      }
    }
    movementDetected = tmp;
  }
}

#endif