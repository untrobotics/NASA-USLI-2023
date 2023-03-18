// https://github.com/govorox/SSLClient needs to be manually installed

#define TINY_GSM_MODEM_SIM7600

// Set serial for debug console (to the Serial Monitor, default speed 115200)
#define SerialMon Serial

#define SerialAT Serial1

// See all AT commands, if wanted
// #define DUMP_AT_COMMANDS

// Define the serial console for debug prints, if needed
#define TINY_GSM_DEBUG SerialMon
// #define LOGGING  // <- Logging is for the HTTP library

// set GSM PIN, if any
#define GSM_PIN ""

// Server details
#include "utilities.h"
String device_id = "seb";

const char apn[] = "h2g2";

#include <SSLClient.h>
#include <TinyGsmClient.h>
#include <ArduinoHttpClient.h>
#include <SPI.h>
#include <SD.h>
#include <Ticker.h>

#ifdef DUMP_AT_COMMANDS
#include <StreamDebugger.h>
StreamDebugger debugger(SerialAT, SerialMon);
TinyGsm        modem(debugger);
#else
TinyGsm        modem(SerialAT);
#endif

TinyGsmClient client(modem, 0);
SSLClient secure_layer(&client);
HttpClient    http(secure_layer, "www.untrobotics.com", 443);

float latitude = 0, longitude = 0, speed = 0, accuracy = 0;
float timer = millis();
bool run_startup = 0;


//optional
void sendStartupTime() 
{
  String httpRequestData = "device_id=" + device_id + "";
  SerialMon.println(httpRequestData);
  String contentType = "application/x-www-form-urlencoded";
  SerialMon.print(F("Performing HTTP POST request... "));
  int err = http.post("/api/rocketry/gps/init", contentType, httpRequestData);
  if (err != 0) {
    SerialMon.println(F("failed to connect"));
    SerialMon.println(err);
    delay(5000);
    return;
  }
  
  Serial.println("success!");

  int status = http.responseStatusCode();
  SerialMon.print(F("Response status code: "));
  SerialMon.println(status);
  if (status != 200) { 
    delay(5000);
    SerialMon.println("Weird");
    return;
  }

  SerialMon.println(F("Response Headers:"));
  while (http.headerAvailable()) {
    String headerName  = http.readHeaderName();
    String headerValue = http.readHeaderValue();
    SerialMon.println("    " + headerName + " : " + headerValue);
  }

  int length = http.contentLength();
  if (length >= 0) {
    SerialMon.print(F("Content length is: "));
    SerialMon.println(length);
  }
  if (http.isResponseChunked()) {
    SerialMon.println(F("The response is chunked"));
  }

  String body = http.responseBody();
  SerialMon.println(F("Response:"));
  SerialMon.println(body);

  SerialMon.print(F("Body length is: "));
  SerialMon.println(body.length());

  if (status == 200)
    run_startup = 1;

  return;
}

void enableGPS(void)
{
  // Set SIM7000G GPIO4 LOW ,turn on GPS power
  // CMD:AT+SGPIO=0,4,1,1
  // Only in version 20200415 is there a function to control GPS power
  modem.sendAT("+SGPIO=0,4,1,1");
  if (modem.waitResponse(10000L) != 1) {
    DBG(" SGPIO=0,4,1,1 false ");
  }
  modem.enableGPS();
}

void disableGPS(void)
{
  // Set SIM7000G GPIO4 LOW ,turn off GPS power
  // CMD:AT+SGPIO=0,4,1,0
  // Only in version 20200415 is there a function to control GPS power
  modem.sendAT("+SGPIO=0,4,1,0");
  if (modem.waitResponse(10000L) != 1) {
    DBG(" SGPIO=0,4,1,0 false ");
  }
  modem.disableGPS();
}

void setup() {
  SerialMon.begin(115200);
  delay(10);

  SerialMon.println("Starting;");
  SerialAT.begin(UART_BAUD, SERIAL_8N1, MODEM_RX, MODEM_TX);

  pinMode(MODEM_PWRKEY, OUTPUT);
  digitalWrite(MODEM_PWRKEY, HIGH);
  delay(300); //Need delay
  digitalWrite(MODEM_PWRKEY, LOW);

  pinMode(MODEM_FLIGHT, OUTPUT);
  digitalWrite(MODEM_FLIGHT, HIGH);

  SerialMon.println("Initializing modem...");
  if (!modem.init()) {
    modem.restart();
    delay(1000);
    Serial.println("Failed to restart modem, attempting to continue without restarting");
    return;
  }

  String ret = modem.setNetworkMode(2);
  DBG("setNetworkMode:", ret);

  String modemInfo = modem.getModemInfo();
  SerialMon.print("Modem Info: ");
  SerialMon.println(modemInfo);

  delay(5000);  
  SerialMon.println("Finished Setup");
}

void loop() {
  SerialMon.println("Looping");

  if (!modem.gprsConnect(apn)) {
    SerialMon.println("Failed GRPS setup");
    delay(1000);
    return;
  }
  if (modem.isGprsConnected()) { SerialMon.println("GPRS connected"); }

  if (!modem.isNetworkConnected()) {
    SerialMon.print("Waiting for network...");
    if (!modem.waitForNetwork()) {
      SerialMon.println(" failed");
      delay(1000);
      return;
    }
    SerialMon.println(" success");
    digitalWrite(LED_PIN, HIGH);
  }
  if (modem.isNetworkConnected()) { SerialMon.println("Network connected"); }
  
  //optional
  if (!run_startup)
    sendStartupTime();

  SerialMon.println("Enabling GPS");
  enableGPS();
  
  float alt;
  int year, month, day, hour, minute, second, vsat, usat;
  while (1) {
    if (modem.getGPS(&latitude, &longitude, &speed, &alt, &vsat, &usat, &accuracy, &year, &month, &day, &hour, &minute, &second)) 
    {
      break;
    }
    delay(2000);
  }
  digitalWrite(LED_PIN, LOW);

  disableGPS();

  delay(1000);

  String httpRequestData = "latitude=" + String(latitude, 6) + "&longitude=" + String(longitude,6) + "&speed=" + String(speed,3) + "&accuracy=" + String(accuracy,4) + "";
  SerialMon.println(httpRequestData);
  String contentType = "application/x-www-form-urlencoded";
  SerialMon.print(F("Performing HTTP POST request... "));
  int err = http.post("/api/rocketry/gps/track", contentType, httpRequestData);
  if (err != 0) {
    SerialMon.println(F("failed to connect"));
    SerialMon.println(err);
    delay(60000);
    return;
  }

  int status = http.responseStatusCode();
  SerialMon.print(F("Response status code: "));
  SerialMon.println(status);
  if (!status) {
    delay(60000);
    return;
  }

  SerialMon.println(F("Response Headers:"));
  while (http.headerAvailable()) {
    String headerName  = http.readHeaderName();
    String headerValue = http.readHeaderValue();
    SerialMon.println("    " + headerName + " : " + headerValue);
  }

  int length = http.contentLength();
  if (length >= 0) {
    SerialMon.print(F("Content length is: "));
    SerialMon.println(length);
  }
  if (http.isResponseChunked()) {
    SerialMon.println(F("The response is chunked"));
  }

  String body = http.responseBody();
  SerialMon.println(F("Response:"));
  SerialMon.println(body);

  SerialMon.print(F("Body length is: "));
  SerialMon.println(body.length());

  //Wait until at least a minute has passed before looping
  while (millis() - timer < 60000)
    delay(1000);
  timer = millis();
}
