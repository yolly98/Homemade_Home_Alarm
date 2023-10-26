#ifndef HEADER
#define HEADER

#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>

#define MOVEMENT_SENSOR 2
#define EXT_LED 3
#define RELAY 4
#define RESET 5

#define SENSOR_ID "24"
#define ROOM  "hall"
#define WIFI_SSID "****"
#define WIFI_PASSW "****"
#define LOCAL_PORT 2390
#define SERVER_IP "192.168.178.32"
#define SERVER_PORT 2390

#define SOLO_MODE 0
#define NET_MODE 1


class CommunicationModule{

  WiFiUDP Udp;
  int status;
  void printWifiStatus();

  public:
    bool initializeUDP();
    void sendPacket(char* data, IPAddress ip, uint16_t port);
    bool receivePacket(char* data, IPAddress* ip, uint16_t* port);
};

extern CommunicationModule communication_module;
#endif