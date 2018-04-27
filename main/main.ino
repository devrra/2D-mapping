// This is the main module.

/*
 * special attention on rotation part
 * ---to ensure that degree of of change of direction in real time matches the 2D mao.
 * 
 * To simply get command for movement.
 * Move according to the command.
 * Send the immediate movement history to the computer.
 * 
 * (COmputer will plot the map according to the input sent by me)
 */

 #include<SoftwareSerial.h>
 SoftwareSerial _2py(10, 11);     //rx,tx
 /* 
  *  input consist of- start command, direction(fore,right,left),degree of rotation(right and left), end command
  *  -91 = forward
  *  0  = no motion 
  *  1 to 90 = anti-clockwise
  *  -1 to -90  =  clockwise
  */

int input;
int i=0;
char gali[3]={'f','l','r'};

void setup() {
  // put your setup code here, to run once:
  
}

void loop() {
  // put your main code here, to run repeatedly:
  seri.write(gali[0]);
  input = seri.read();
  Serial.println(input);
  delay(500);

}
