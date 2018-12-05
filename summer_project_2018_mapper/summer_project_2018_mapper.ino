#include <SoftwareSerial.h>
SoftwareSerial ArduinoUno(13,12);
//mazerunner
int ipmd1=3 ,ipmd2=2,ipmd3=4,ipmd4=5,trig1=8,echo1=9,trig2=6,echo2=7,trig3=11,echo3=10;
//us1=front,us2=right,us3=left
void setup(){
pinMode(ipmd1,OUTPUT);//motorpart
pinMode(ipmd2,OUTPUT);
pinMode(ipmd3,OUTPUT);
pinMode(ipmd4,OUTPUT);
pinMode(trig1,OUTPUT);//USpart
pinMode(echo1,INPUT);
pinMode(trig2,OUTPUT);
pinMode(echo2,INPUT);
pinMode(trig3,OUTPUT);
pinMode(echo3,INPUT);
Serial.begin(9600);
ArduinoUno.begin(4800);
}
void NodeMCU(int a);
int distance1();
int distance2();
int distance3();
void left();
void right();
void straight();
void stopper();
int dis1,dis2,dis3,i=0;
void loop(){
dis1=distance1();
dis2=distance2();
dis3=distance3();
if(dis1<=15){
  stopper();
if(dis2>=10&&dis3>=10){
//i++;
right();
/*switch(i){//thisisusedforTpositions,differentcasesforwhattobedoneatdifferentTs
case1:
right();
break;
case2:
left();
break;
case3:
left();
break;
case4:
right();
break;
}*/
}
else if(dis2>=10){
right();//delaygiveninthefunction
}
else{
left();
}
}
else{
straight();
}
}
int distance1(){
int duration,d;
digitalWrite(trig1,HIGH);
delayMicroseconds(2000);//checkthis
digitalWrite(trig1,LOW);
duration=pulseIn(echo1,HIGH);
d=((duration*0.0345)/2);
Serial.print(d);
Serial.print("cm1");
return(d);}
int distance2(){
int duration,d;
digitalWrite(trig2,HIGH);
delayMicroseconds(2000);//checkthis
digitalWrite(trig2,LOW);
duration=pulseIn(echo2,HIGH);
d=((duration*0.0345)/2);
//Serial.print(d);
//Serial.print("cm2");
return(d);}
int distance3(){
int duration,d;
digitalWrite(trig3,HIGH);
delayMicroseconds(2000);//checkthis
digitalWrite(trig3,LOW);
duration=pulseIn(echo3,HIGH);
d=((duration*0.0345)/2);
//Serial.print(d);
//Serial.print("cm3");
return(d);}

void straight(){
NodeMCU(1);
digitalWrite(ipmd1,HIGH);
digitalWrite(ipmd2,LOW);
digitalWrite(ipmd3,HIGH);
digitalWrite(ipmd4,LOW);
//checkifthispositionrequiresadelayandalsowhetheryouneedtowritealowtoallpins
//againhere
}
void left(){
NodeMCU(3);  
digitalWrite(ipmd1,HIGH);
digitalWrite(ipmd2,LOW);
digitalWrite(ipmd4,HIGH);
digitalWrite(ipmd3,LOW);
delay(450);
digitalWrite(ipmd1,LOW);
digitalWrite(ipmd2,LOW);
digitalWrite(ipmd3,LOW);
digitalWrite(ipmd4,LOW);
}
void right(){
NodeMCU(2);  
digitalWrite(ipmd1,LOW);
digitalWrite(ipmd2,HIGH);
digitalWrite(ipmd4,LOW);
digitalWrite(ipmd3,HIGH);
delay(450);
digitalWrite(ipmd1,LOW);
digitalWrite(ipmd2,LOW);
digitalWrite(ipmd3,LOW);
digitalWrite(ipmd4,LOW);
}
void stopper(){
NodeMCU(4);  
digitalWrite(ipmd1,LOW);
digitalWrite(ipmd2,LOW);
digitalWrite(ipmd3,LOW);
digitalWrite(ipmd4,LOW);
}
void NodeMCU(int a){
  ArduinoUno.print(a);
  ArduinoUno.println("\n");
}

