#ifndef HEADER
#define HEADER

#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>

#define SENSOR_ID "24"
#define ROOM  "hall"
#define WIFI_SSID "****"
#define WIFI_PASSW "****"
#define LOCAL_PORT 2390

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