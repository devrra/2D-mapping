/*
*Author(s) 		    : Pradymna Gupta, Yash Raj
*Functions 			  : setup_wifi, reconnect, setup, loop, I2C_Write, Read_RawValue, MPU6050_Init
*Global Variables	: ssid, password, mqtt_server, MPU6050SlaveAddress, scl, sda, AccelScaleFactor, GyroScaleFactor,
                    AccelX, AccelY, AccelZ, Temperature, GyroX, GyroY, GyroZ, timePast, timePresent, gyroXCalli, 
                    gyroYCalli, gyroZCalli, AccelCalli, velocityPresent, velocityPast, Ax, Ay, Az, T, Gx, Gy, Gz
                    GyroXPast, GyroYPast, GyroZPast, angleX, angleY, angleZ, distance
*/

#include <ESP8266WiFi.h>    // Library for using the NodeMCU 
#include <PubSubClient.h>   // Library for using the Network protcall MQTT in this case
#include <Wire.h>           // lib for communication.
#include "ArduinoJson.h"      

/************************* WiFi Access Point *********************************/


const char* ssid = "will"; // Add your SSID
const char* password = "12345678"; // The PassWord (Wireless Key)
                  
/************************* LinuxMqtt Setup *********************************/

const char* mqtt_server = "broker.mqtt-dashboard.com";
WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(100);
  // We start by connecting to a WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    //if you MQTT broker has clientID,username and password
    //please change following line to    if (client.connect(clientId,userName,passWord))
    if (client.connect(clientId.c_str()))
    {
      Serial.println("connected");

    }
    else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 6 seconds before retrying
      delay(6000);
    }
  }
} 

//******************************* Setting Up mpu **************************************

// MPU6050 Slave Device Address
const uint8_t MPU6050SlaveAddress = 0x68;

// Select SDA and SCL pins for I2C communication 
const uint8_t scl = D6;
const uint8_t sda = D7;

// sensitivity scale factor respective to full scale setting provided in datasheet 
const uint16_t AccelScaleFactor = 16384;
const uint16_t GyroScaleFactor = 131;

// MPU6050 few configuration register addresses
const uint8_t MPU6050_REGISTER_SMPLRT_DIV   =  0x19;
const uint8_t MPU6050_REGISTER_USER_CTRL    =  0x6A;
const uint8_t MPU6050_REGISTER_PWR_MGMT_1   =  0x6B;
const uint8_t MPU6050_REGISTER_PWR_MGMT_2   =  0x6C;
const uint8_t MPU6050_REGISTER_CONFIG       =  0x1A;
const uint8_t MPU6050_REGISTER_GYRO_CONFIG  =  0x1B;
const uint8_t MPU6050_REGISTER_ACCEL_CONFIG =  0x1C;
const uint8_t MPU6050_REGISTER_FIFO_EN      =  0x23;
const uint8_t MPU6050_REGISTER_INT_ENABLE   =  0x38;
const uint8_t MPU6050_REGISTER_ACCEL_XOUT_H =  0x3B;
const uint8_t MPU6050_REGISTER_SIGNAL_PATH_RESET  = 0x68;

int16_t AccelX, AccelY, AccelZ, Temperature, GyroX, GyroY, GyroZ,timePast,timePresent;
static double gyroXCalli=0,gyroYCalli=0,gyroZCalli=0,AccelCalli=0,velocityPresent=0,velocityPast=0;
static double Ax, Ay, Az, T, Gx, Gy, Gz;
static double GyroXPast=0,GyroYPast=0,GyroZPast=0,angleX=0,angleY=0,angleZ=0,distance=0;

//*************************************************************************************
void setup() {
  Serial.begin(115200);     // Starts the serial monitor at 115200
  setup_wifi();       // add Method for the Wifi setup
  client.setServer(mqtt_server, 1883);  // connects to the MQTT broker
  Wire.begin(sda, scl);
  MPU6050_Init();
}

void loop() {

  if (!client.connected()) {
    reconnect();
  } 

  double Ax, Ay, Az, T, Gx, Gy, Gz;
  Read_RawValue(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_XOUT_H);
  Ax = (double)(AccelX-AccelCalli)/AccelScaleFactor;
  Ay = (double)AccelY/AccelScaleFactor;
  Az = (double)AccelZ/AccelScaleFactor;
  T = (double)Temperature/340+36.53; //temperature formula
  Gx = (double)(GyroX-gyroXCalli)/GyroScaleFactor;
  Gy = (double)(GyroY-gyroYCalli)/GyroScaleFactor;
  Gz = (double)(GyroZ-gyroZCalli)/GyroScaleFactor;

  Serial.print(" Ax: "); Serial.print(Ax);
  Serial.print(" Ay: "); Serial.print(Ay);
  Serial.print(" Az: "); Serial.print(Az);
  Serial.print(" T: "); Serial.print(T);
  Serial.print(" Gx: "); Serial.print(Gx);
  Serial.print(" Gy: "); Serial.print(Gy);
  Serial.print(" Gz: "); Serial.println(Gz);
 
//*********************** JSON ****************************************

//StaticJsonBuffer<300> JSONbuffer;
//JsonObject& JSONencoder = JSONbuffer.createObject();
//JSONencoder["Ax"] = Ax;
//JSONencoder["Ay"] = Ay;
//JSONencoder["Az"] = Az;
//JSONencoder["Gx"] = Ax;
//JSONencoder["Gy"] = Gy;
//JSONencoder["Gz"] = Gz;
//
////JSONencoder.prettyPrintTo(Serial);
//
//char JSONmessageBuffer[100];
//JSONencoder.printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
//Serial.println(JSONmessageBuffer);
String JSON = "{";
JSON += "\'Ax\' : " + String(Ax) + ",";
JSON += "\'Ay\' : " + String(Ay) + ",";
JSON += "\'Az\' : " + String(Az) + ",";
JSON += "\'Gx\' : " + String(Gx) + ",";
JSON += "\'Gy\' : " + String(Gy) + ",";
JSON += "\'Gz\' : " + String(Gz);
JSON += "}";
/************************* Publish String MQTT ************************/

  //client.publish("meena", JSONmessageBuffer);
  client.publish("meena", JSON.c_str());
  delay(200);
}

void I2C_Write(uint8_t deviceAddress, uint8_t regAddress, uint8_t data){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.write(data);
  Wire.endTransmission();
}

void Read_RawValue(uint8_t deviceAddress, uint8_t regAddress){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.endTransmission();
  Wire.requestFrom(deviceAddress, (uint8_t)14);
  AccelX = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelY = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelZ = (((int16_t)Wire.read()<<8) | Wire.read());
  Temperature = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroX = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroY = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroZ = (((int16_t)Wire.read()<<8) | Wire.read());
}

void MPU6050_Init(){
  delay(150);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SMPLRT_DIV, 0x07);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_1, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_2, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_CONFIG, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_GYRO_CONFIG, 0x00);//set +/-250 degree/second full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_CONFIG, 0x00);// set +/- 2g full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_FIFO_EN, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_INT_ENABLE, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SIGNAL_PATH_RESET, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_USER_CTRL, 0x00);
}
