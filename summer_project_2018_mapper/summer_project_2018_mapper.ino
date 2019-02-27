/*
Authors           : Pradyumna Gupta, Yash Raj
Purpose of Code   : 
Global Variables  : ipmd(1/2/3/4), echo(1/2/3), trig(1/2/3), dis(1/2/3), i 
Functions         : setup, loop, NodeMCU, distance1, distance2, distance3, left, right, straight, stopper
*/

#include <SoftwareSerial.h>
SoftwareSerial ArduinoUno(13,12);
//mazerunner
int ipmd1=3 ,ipmd2=2,ipmd3=4,ipmd4=5,trig1=8,echo1=9,trig2=6,echo2=7,trig3=11,echo3=10;
//us1=front,us2=right,us3=left

/*
Name      : setup(its mandatory function in extended C, called only once)
input(s)  : None
output(s) : None(called to configure pinmodes etc.. in arduino micro-controller)
*/
void setup()
{
  //motor pins configured
  pinMode(ipmd1,OUTPUT);
  pinMode(ipmd2,OUTPUT);
  pinMode(ipmd3,OUTPUT);
  pinMode(ipmd4,OUTPUT);
  //Ultra Sound sensors configured
  pinMode(trig1,OUTPUT);
  pinMode(echo1,INPUT);
  pinMode(trig2,OUTPUT);
  pinMode(echo2,INPUT);
  pinMode(trig3,OUTPUT);
  pinMode(echo3,INPUT);
  
  Serial.begin(9600);
  //To communicate with nodeMCU
  ArduinoUno.begin(4800);
}

//Function signatures
void NodeMCU(int a);
int distance1();
int distance2();
int distance3();
void left();
void right();
void straight();
void stopper();

//distance observed by ultrasound sensors
int dis1,dis2,dis3,i=0;

/*
Name      : setup(its mandatory function in extended C, called only once)
input(s)  : None
output(s) : None(called to configure pinmodes etc.. in arduino micro-controller)
*/
void loop()
{
  dis1=distance1();
  dis2=distance2();
  dis3=distance3();
  //condition driven decisions for motion
  if(dis1<=15)
  {
    stopper();
    if(dis2>=10&&dis3>=10)
    {
      //i++;
      right();
      /*
      switch(i)
      {//thisisusedforTpositions,differentcasesforwhattobedoneatdifferentTs
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
      }
      */
    }
    else if(dis2>=10)
    {
      right();//delaygiveninthefunction
    }
    else
    {
      left();
    }
  }
  else
  {
    straight();
  }
}

/*
Name      : distance1
input(s)  : None
output(s) : distance measured by ultrasound sensor 1
*/
int distance1()
{
  int duration,d;
  digitalWrite(trig1,HIGH);
  delayMicroseconds(2000);//checkthis
  digitalWrite(trig1,LOW);
  duration=pulseIn(echo1,HIGH);
  d=((duration*0.0345)/2);
  Serial.print(d);
  Serial.print("cm1");
  return(d);
}

/*
Name      : distance2
input(s)  : None
output(s) : distance measured by ultrasound sensor 2
*/
int distance2()
{
  int duration,d;
  digitalWrite(trig2,HIGH);
  delayMicroseconds(2000);//checkthis
  digitalWrite(trig2,LOW);
  duration=pulseIn(echo2,HIGH);
  d=((duration*0.0345)/2);
  //Serial.print(d);
  //Serial.print("cm2");
  return(d);
}

/*
Name      : distance3
input(s)  : None
output(s) : distance measured by ultrasound sensor 3
*/
int distance3()
{
  int duration,d;
  digitalWrite(trig3,HIGH);
  delayMicroseconds(2000);//checkthis
  digitalWrite(trig3,LOW);
  duration=pulseIn(echo3,HIGH);
  d=((duration*0.0345)/2);
  //Serial.print(d);
  //Serial.print("cm3");
  return(d);
}

/*
Name      : straight
input(s)  : None
output(s) : None (commands the bot to move ahead)
*/
void straight()
{
  NodeMCU(1);
  digitalWrite(ipmd1,HIGH);
  digitalWrite(ipmd2,LOW);
  digitalWrite(ipmd3,HIGH);
  digitalWrite(ipmd4,LOW);
  //checkifthispositionrequiresadelayandalsowhetheryouneedtowritealowtoallpins
  //againhere
}

/*
Name      : left
input(s)  : None
output(s) : None (commands the bot to move left)
*/
void left()
{
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

/*
Name      : right
input(s)  : None
output(s) : None (commands the bot to move right)
*/
void right()
{
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

/*
Name      : stopper
input(s)  : None
output(s) : None (commands the bot to stop)
*/
void stopper()
{
  NodeMCU(4);  
  digitalWrite(ipmd1,LOW);
  digitalWrite(ipmd2,LOW);
  digitalWrite(ipmd3,LOW);
  digitalWrite(ipmd4,LOW);
}

/*
Name      : NodeMCU
input(s)  : integer 
output(s) : None (commands the bot to move stopper)
*/
void NodeMCU(int a)
{
  ArduinoUno.print(a);
  ArduinoUno.println("\n");
}
