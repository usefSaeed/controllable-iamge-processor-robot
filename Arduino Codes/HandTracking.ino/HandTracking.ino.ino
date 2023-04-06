#include <Servo.h>
#define servoPin 14

Servo myservo;
String inByte;
int pos;

void setup()
{
Serial.begin(9600);
myservo.attach(servoPin);
}

void loop()
{
  if(Serial.available())
  {
    inByte = Serial.readStringUntil('\n');
    pos = inByte.toInt();
    pos = map(pos,1,5,0,180);
//    Serial.println(pos);
    myservo.write(pos);
}
}
