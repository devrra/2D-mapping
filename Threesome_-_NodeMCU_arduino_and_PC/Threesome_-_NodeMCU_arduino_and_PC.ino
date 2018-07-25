#include<ESP8266WiFi.h>
#include <SoftwareSerial.h>
const char* ssid="will";
const char* password="12345678";
WiFiServer server(80);
SoftwareSerial NodeMCU(D2,D3);
void setup() 
{
Serial.begin(115200);  /* initialise serial communication */
Serial.println();
Serial.println();
Serial.print("connnecting to");
Serial.print(ssid);
WiFi.begin(ssid,password);
while(WiFi.status()!=WL_CONNECTED){
  digitalWrite(D4,LOW);
  delay(500);
  Serial.print(".");
  digitalWrite(D4,HIGH);
}
digitalWrite(D4,HIGH);
Serial.println(" ");
Serial.println("WiFi Connected");
server.begin();
Serial.println("Server started");
Serial.println(WiFi.localIP());
NodeMCU.begin(4800);
  pinMode(D2,INPUT);
  pinMode(D3,OUTPUT);
  pinMode(D4,OUTPUT);
  digitalWrite(D4,HIGH);
}

void loop()
{
WiFiClient client=server.available();
if(!client)
return;
Serial.println("new client");
while(!client.available()){
  delay(1);
}
/*int i=0;
while(i<10){
  client.println("yo boy");
  i++;
  delay(20);
}*/
while(NodeMCU.available()>0){
  float val = NodeMCU.parseFloat();
  if(NodeMCU.read()== '\n'){
  Serial.println(val);
  if((int)val==1)
  client.println("straight\n");
  else if((int)val==2)
  client.println("right\n");
  else if((int)val==3)
  client.println("left\n");
  else client.println("stopped\n");
   digitalWrite(D4,LOW);
   delay(2);
   digitalWrite(D4,HIGH);
   delay(2);
    }
  }
}

