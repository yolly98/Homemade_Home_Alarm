#ifndef SENSOR_NODE_ALARM
#define SENSOR_NODE_ALARM

#include "sensor_node_alarm.h"

CommunicationModule communicationModule;

void setup(){
  
  Serial.begin(9600);
  while(!Serial);

  communicationModule.initializeUDP();
}

void loop(){

  IPAddress ip;
  uint16_t port;
  char receivedPacket[256];

  if ( communicationModule.receivePacket(receivedPacket, &ip, &port)){

    Serial.print("IP: ");
    Serial.println(ip);
    Serial.print("PORT: ");
    Serial.println(port);
    Serial.print("Contents: ");
    Serial.println(receivedPacket);

    char ackPacket[256] = "ACK";
    communicationModule.sendPacket(ackPacket, ip, port);
  }

}


#endif