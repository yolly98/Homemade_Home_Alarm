#ifndef SENSOR_NODE_ALARM
#define SENSOR_NODE_ALARM

#include "sensor_node_alarm.h"

#define MOVEMENT_SENSOR 2
#define EXT_LED 3
#define RELAY 4
#define RESET 5

uint8_t MODE = SOLO_MODE;

CommunicationModule communicationModule;

void setup(){
  
  pinMode(LEDR, OUTPUT);
  pinMode(LEDB, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(MOVEMENT_SENSOR, INPUT);
  pinMode(EXT_LED, OUTPUT);
  pinMode(RELAY, OUTPUT);
  pinMode(RESET, OUTPUT);

  digitalWrite(RESET, HIGH);
  digitalWrite(RELAY, HIGH);
  digitalWrite(EXT_LED, LOW);
  digitalWrite(LEDR, HIGH);
  digitalWrite(LEDB, HIGH);
  digitalWrite(LEDG, HIGH);
  Serial.begin(9600);
  while(!Serial);

  communicationModule.initializeUDP();

  delay(1000);

  char packet[256];
  sprintf(packet, "/%s/%s/INIT",ROOM, SENSOR_ID);

  int max_attempts = 3;
  while(max_attempts > 0){
    communicationModule.sendPacket(packet, (IPAddress)SERVER_IP, (uint16_t)SERVER_PORT);
    delay(5000);

    IPAddress ip;
    uint16_t port;
    char receivedPacket[256];
    if (communicationModule.receivePacket(receivedPacket, &ip, &port)){

      Serial.print("IP: ");
      Serial.println(ip);
      Serial.print("PORT: ");
      Serial.println(port);
      Serial.print("Contents: ");
      Serial.println(receivedPacket);

      if(strcmp(receivedPacket, "ACK") == 0){
        MODE = NET_MODE;
        digitalWrite(LEDR, LOW);
        digitalWrite(LEDG, LOW);
        digitalWrite(LEDB, HIGH);
        break;
      } else{
        break;
      }
    }
    max_attempts--;
  }
  if(MODE == SOLO_MODE){
    digitalWrite(LEDR, LOW);
    digitalWrite(LEDG, HIGH);
    digitalWrite(LEDB, LOW);
  }

}

void loop(){

  IPAddress ip;
  uint16_t port;
  char receivedPacket[256];

  if (communicationModule.receivePacket(receivedPacket, &ip, &port)){

    Serial.print("IP: ");
    Serial.println(ip);
    Serial.print("PORT: ");
    Serial.println(port);
    Serial.print("Contents: ");
    Serial.println(receivedPacket);

    char ackPacket[256] = "ACK";
    communicationModule.sendPacket(ackPacket, ip, (uint16_t)SERVER_PORT);
    delay(1000);

    if(strcmp(receivedPacket, "RESTART") == 0)
      digitalWrite(RESET, LOW);
    else if(strcmp(receivedPacket, "START") == 0)
      digitalWrite(RELAY, LOW);
    else if(strcmp(receivedPacket, "END") == 0)
      digitalWrite(RELAY, HIGH);
  }

  if(digitalRead(MOVEMENT_SENSOR) == HIGH) // no movements detected
    digitalWrite(EXT_LED, HIGH);
  else // movement detected
    digitalWrite(EXT_LED, LOW);
}


#endif