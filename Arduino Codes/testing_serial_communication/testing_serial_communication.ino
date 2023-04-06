#include <Servo.h>
#define Current_sensor A7  //The sensor analog input pin
float i;
#define Vsens A6
#define Wsens 13
float voltage = 0;
Servo myservo;
String inByte;
int pos;

int serialData;
String serialData1;
int arr[3];
int pin = 10;
int pin1 = A0;

int pin2 = 13;
int pin3 = A5;
int pin4 = A4;
int pin5 = 7;
int pin6 = 8;
int pin7 = 9;
int speed;
int servoPin = 11;
int pwm4 = 6;
Servo ESC1;
Servo ESC2;
int key;
int mood;
int value;
int value1;
int value2;
int speedd;
void setup() {
  pinMode(pin1, OUTPUT); 
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);
  pinMode(pin5, OUTPUT);
  pinMode(pin6, OUTPUT);
  pinMode(pin7, OUTPUT);
  pinMode(Current_sensor, INPUT);
  myservo.attach(servoPin);

  pinMode(Vsens, INPUT);
  pinMode(Wsens, INPUT);
  pinMode(pwm4, OUTPUT);
  ESC1.attach(5, 1000, 2000);
  ESC2.attach(3, 1000, 2000);
  // put your setup code here, to run once:
  pinMode(pin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available()) {
    voltage = analogRead(Vsens) * (5.0/1023)*((100+10)/10);
  Serial.println('v' + String(voltage,3));
    if (digitalRead(Wsens) == HIGH)
  {
    Serial.println("Yes");
  } 
  else 
  {
    Serial.println("No ");
  }
    
    i = analogRead(Current_sensor);
    Serial.println('c' + String(i));
    serialData1 = Serial.readString();
    
    

    speedd = serialData1[0];
    mood = serialData1[1];
    key = serialData1[2];
    inByte = serialData1[3];
    pos = inByte.toInt();
    pos = map(pos,1,5,0,180);
    myservo.write(pos); 
    digitalWrite(pin, HIGH);

    if (speedd == 'x') {
      speed = 50;
      digitalWrite(pin5, HIGH);
      digitalWrite(pin6, LOW);
      digitalWrite(pin7, LOW);
      digitalWrite(pin, HIGH);
    } else if (speedd == 'y') {
      digitalWrite(pin5, LOW);
      digitalWrite(pin6, HIGH);
      digitalWrite(pin7, LOW);
      speed = 150;
    } else if (speedd == 'z') {
      digitalWrite(pin5, LOW);
      digitalWrite(pin6, LOW);
      digitalWrite(pin7, HIGH);
      speed = 255;

    }
    value = speed / 2;
    if (mood == 'm') {
      digitalWrite(pin, HIGH); //dc motor will only work
      if (key == 'u') {
        digitalWrite(pin1, HIGH);
        digitalWrite(pin3, HIGH);
        digitalWrite(pin2, LOW);
        digitalWrite(pin4, LOW);
        analogWrite(pwm4, speed);
        digitalWrite(pin, HIGH);

      }
      else if (key == 'd') {
        digitalWrite(pin2, HIGH);
        digitalWrite(pin3, LOW);
        digitalWrite(pin1, LOW);
        digitalWrite(pin4, HIGH);
        analogWrite(pwm4, speed);

      } else if (key == 'l') {
        digitalWrite(pin1, HIGH);
        digitalWrite(pin3, LOW);
        digitalWrite(pin2, LOW);
        digitalWrite(pin4, LOW);
        analogWrite(pwm4, speed);

      } else if (key == 'r') {
        digitalWrite(pin1, LOW);
        digitalWrite(pin3, HIGH);
        digitalWrite(pin2, LOW);
        digitalWrite(pin4, LOW);
        analogWrite(pwm4, speed);
      }

    }
    else if (mood == 'b') { //brushless motors are working
      if (key == 'u') {
        value1 = map(value, 0, 127, 0, 90);
        ESC1.write(value1);
        ESC2.write(value1);
      }
      else if (key == 'd') {
        value2 = map(value, 0, 127, 90, 180);
        ESC1.write(value2);
        ESC2.write(value2);
      } else if (key == 'l') {
        value1 = map(value, 0, 127, 0, 90);
        ESC1.write(value1);
        ESC2.write(0);
      } else if (key == 'r') {
        value1 = map(value, 0, 127, 0, 90);
        ESC1.write(0);
        ESC2.write(speed);

      }
    }

  }
}
