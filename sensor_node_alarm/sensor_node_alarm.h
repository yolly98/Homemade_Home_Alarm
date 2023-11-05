#ifndef HEADER
#define HEADER

#include <SPI.h>

#define WIFI_NINA
#ifdef WIFI_NINA
  #include <WiFiNINA.h>
  #include <WiFiUdp.h>
#endif
#ifdef WIFI_ESP32S3
  #include <WiFiS3.h>
#endif

#include "secrets.h"

#define MOVEMENT_SENSOR 2
#define EXT_LED 3
#define RELAY 4
#define RESET 5

#define SENSOR_ID "1"
#define ROOM  "hall"
#define WIFI_SSID MY_WIFI_SSID
#define WIFI_PASSW MY_WIFI_PASSW
#define LOCAL_PORT 2390
#define SERVER_IP "192.168.178.33"
#define SERVER_PORT 2390
#define COMMUNICATION_ATTEMPTS 3
#define SENDING_DELAY 1000
#define ACTIVATION_DELAY 30000
#define EXT_LED_BLINK_INTERVAL 500
#define PACKET_SIZE 50
#define KEEP_ALIVE_TIMER 1000 * 60 * 10
#define SOLO_MODE 0
#define NET_MODE 1

enum Colors { Red = 0, Blue = 1, Green = 2, White = 3, Off = 4};

class LedStatusModule{

  Colors status;
  
  public:
  void init();
  void set(Colors color);
  Colors getStatus();
};

class CommunicationModule{

  WiFiUDP Udp;
  int status;
  void printWifiStatus();

  public:
    bool initializeUDP();
    void sendPacket(char* data, IPAddress ip, uint16_t port);
    bool receivePacket(char* data, IPAddress* ip, uint16_t* port);
};

class MovementSensor{

  bool status;

  public:
  void init();
  void activateAlarm();
  void deactivateAlarm();
  bool check();
  bool getStatus();
};

#endif