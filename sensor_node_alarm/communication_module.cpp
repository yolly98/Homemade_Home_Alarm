#ifndef COMMUNICATION_MODULE
#define COMMUNICARION_MODULE

#include "sensor_node_alarm.h"

bool CommunicationModule::initializeUDP(){

  if (WiFi.status() == WL_NO_MODULE) {
    // Serial.println("Communication with WiFi module failed!");
    return false;
  }

  String fv = WiFi.firmwareVersion();

  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the WIFI firmware");
  }

  // attempt to connect to Wifi network:
  connectToRouter();

  Serial.println("Connected to wifi");
  // printWifiStatus();
  Udp.begin(LOCAL_PORT);
  delay(1000);
  
  return true;
} 

void CommunicationModule::connectToRouter(){
  
  while (WiFi.status() != WL_CONNECTED) {

    Serial.print("Attempting to connect to SSID: ");
    Serial.println(WIFI_SSID);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    WiFi.begin(WIFI_SSID, WIFI_PASSW);
    delay(10000);
  } 
}


void CommunicationModule::sendPacket(char* data, IPAddress ip, uint16_t port){

    connectToRouter(); // if the connection is lost, the node tries to connect again
    Udp.beginPacket(ip, port);
    Udp.write(data);
    Udp.endPacket();

}

bool CommunicationModule::receivePacket(char* packetBuffer, IPAddress* ip, uint16_t* port){

  connectToRouter(); // if the connection is lost, the node tries to connect again
  int packetSize = Udp.parsePacket();

  if (packetSize) {

    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer, PACKET_SIZE);
    if (len > 0) {
      packetBuffer[len] = 0;
    }

    *ip = Udp.remoteIP();
    *port = Udp.remotePort();

    Serial.print("IP: ");
    Serial.println(*ip);
    Serial.print("PORT: ");
    Serial.println(*port);
    Serial.print("Contents: ");
    Serial.println(packetBuffer);

    return true;
  }
  else
    return false;
}

void CommunicationModule::printWifiStatus(){

  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

#endif