#include <Wire.h>

long accelX, accelY, accelZ;
float gForceX=0, gForceY=0, gForceZ=0;
float distance=0;
float velocityPast=0,velocityPresent=0,AccelCalli=0,gForcePast=0;;
long gyroXCalli = 0, gyroYCalli = 0, gyroZCalli = 0;
long gyroXPresent = 0, gyroYPresent = 0, gyroZPresent = 0;
long gyroXPast = 0, gyroYPast = 0, gyroZPast = 0;
float rotX, rotY, rotZ;

float angelX = 0, angelY = 0, angelZ = 0;

long timePast = 0;
long timePresent = 0;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  setUpMPU();
  callibrateGyroValues();
  callibrateAccelValues();
  timePresent = millis();
}

void loop() {
  //Serial.print(" Accel (g)");
  readAndProcessAccelData();
  readAndProcessGyroData();
  printData();
  delay(10);
}

void setUpMPU() {
  // power management
  Wire.beginTransmission(0b1101000);          // Start the communication by using address of MPU
  Wire.write(0x6B);                           // Access the power management register
  Wire.write(0b00000000);                     // Set sleep = 0
  Wire.endTransmission();                     // End the communication

  // configure gyro
  Wire.beginTransmission(0b1101000);
  Wire.write(0x1B);                           // Access the gyro configuration register
  Wire.write(0b00000000);
  Wire.endTransmission();

  // configure accelerometer
  Wire.beginTransmission(0b1101000);
  Wire.write(0x1C);                           // Access the accelerometer configuration register
  Wire.write(0b00000000);
  Wire.endTransmission();  
}

void callibrateGyroValues() {
    for (int i=0; i<5000; i++) {
      getGyroValues();
      gyroXCalli = gyroXCalli + gyroXPresent;
      gyroYCalli = gyroYCalli + gyroYPresent;
      gyroZCalli = gyroZCalli + gyroZPresent;
    }
    gyroXCalli = gyroXCalli/5000;
    gyroYCalli = gyroYCalli/5000;
    gyroZCalli = gyroZCalli/5000;
}
void callibrateAccelValues() {
    for (int i=0; i<5000; i++) {
      readAndProcessAccelData();
      AccelCalli = AccelCalli + gForceX;
    }
    AccelCalli = AccelCalli/5000.0;
}
void readAndProcessAccelData() {
  velocityPast=velocityPresent;
  gForcePast=gForceX;
  timePast=timePresent;
  timePresent=millis();
  Wire.beginTransmission(0b1101000); 
  Wire.write(0x3B); 
  Wire.endTransmission();
  Wire.requestFrom(0b1101000,6); 
  while(Wire.available() < 6);
  accelX = Wire.read()<<8|Wire.read(); 
  accelY = Wire.read()<<8|Wire.read(); 
  accelZ = Wire.read()<<8|Wire.read(); 
  processAccelData();
}

void processAccelData() {
  gForceX = accelX/16384.0;
  gForceY = accelY/16384.0; 
  gForceZ = accelZ/16384.0;
  float temp=gForceX-AccelCalli;
  temp=(temp+abs(temp))/2.0;
  velocityPresent=velocityPast+temp*9.8*(timePresent-timePast)*0.001;
  //Serial.print("velpre=");
  //Serial.print(velocityPresent);
  //Serial.print("velpas=");
  //Serial.println(velocityPast);
}

void readAndProcessGyroData() {
  gyroXPast = gyroXPresent;                                   // Assign Present gyro reaging to past gyro reading
  gyroYPast = gyroYPresent;                                   // Assign Present gyro reaging to past gyro reading
  gyroZPast = gyroZPresent;                                   // Assign Present gyro reaging to past gyro reading
  timePast = timePresent;                                     // Assign Present time to past time
  timePresent = millis();                                     // get the current time in milli seconds, it is the present time
  
  getGyroValues();                                            // get gyro readings
  getAngularVelocity();                                       // get angular velocity
  calculateAngle();                                           // calculate the angle  
}

void getGyroValues() {
  Wire.beginTransmission(0b1101000);                          // Start the communication by using address of MPU 
  Wire.write(0x43);                                           // Access the starting register of gyro readings
  Wire.endTransmission();
  Wire.requestFrom(0b1101000,6);                              // Request for 6 bytes from gyro registers (43 - 48)
  while(Wire.available() < 6);                                // Wait untill all 6 bytes are available
  gyroXPresent = Wire.read()<<8|Wire.read();                  // Store first two bytes into gyroXPresent
  gyroYPresent = Wire.read()<<8|Wire.read();                  // Store next two bytes into gyroYPresent
  gyroZPresent = Wire.read()<<8|Wire.read();                  //Store last two bytes into gyroZPresent
}

void getAngularVelocity() {
  rotX = gyroXPresent / 131.0;                                
  rotY = gyroYPresent / 131.0; 
  rotZ = gyroZPresent / 131.0;
}

void calculateAngle() {  
  // same equation can be written as 
  // angelZ = angelZ + ((timePresentZ - timePastZ)*(gyroZPresent + gyroZPast - 2*gyroZCalli)) / (2*1000*131);
  // 1/(1000*2*131) = 0.00000382
  // 1000 --> convert milli seconds into seconds
  // 2 --> comes when calculation area of trapezium
  // substacted the callibated result two times because there are two gyro readings
  float temp=gForceX-AccelCalli;
  temp=(temp+abs(temp))/2.0;
  angelX = angelX + ((timePresent - timePast)*(gyroXPresent + gyroXPast - 2*gyroXCalli)) * 0.00000382;
  angelY = angelY + ((timePresent - timePast)*(gyroYPresent + gyroYPast - 2*gyroYCalli)) * 0.00000382;
  angelZ = angelZ + ((timePresent - timePast)*(gyroZPresent + gyroZPast - 2*gyroZCalli)) * 0.00000382;
  distance=distance+((timePresent - timePast)*velocityPast*0.001+0.5*temp*9.8*(timePresent - timePast)*(timePresent - timePast)*0.001*0.001);
  Serial.print("dist=");
  Serial.print(0.5*temp*9.8*(timePresent - timePast)*(timePresent - timePast)*0.001*0.001);
  Serial.print("delay=");
  Serial.print(timePresent - timePast);
}

void printData() {
  /*Serial.print("Gyro(deg/sec)");
  Serial.print("X=");
  Serial.print(rotX);
  Serial.print("Y=");
  Serial.print(rotY); 
  //Serial.print("Angle (deg)");
  Serial.print("Z=");
  Serial.println(rotZ);*/

  Serial.print("Angulardisplacementwrtstartedposition (deg)");
  Serial.print("X =");
  Serial.print(angelX);
  Serial.print(" Y=");
  Serial.print(angelY);
  Serial.print(" Z=");
  Serial.print(angelZ);
  Serial.print(" Present=");
  Serial.print(gyroYPresent);
  Serial.print(" Past=");
  Serial.print(gyroYPast);
  Serial.print("distance=");
  Serial.print(distance);
  
  Serial.print("X=");
  Serial.println(gForceX-AccelCalli);
    
  /*Serial.print("Acceleratio (g)");
  Serial.print("X=");
  Serial.print(gForceX);
  Serial.print("Y=");
  Serial.print(gForceY);
  Serial.print("Z=");
  Serial.println(gForceZ);*/
}
