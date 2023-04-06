/*This code works with ACS712 Current sensor, it permits to read the raw data
  It's better to use it with Serial Plotter
  More details on www.surtrtech.com
*/

#define Current_sensor 20  //The sensor analog input pin

float i;


void setup() {

Serial.begin(9600);
pinMode(Current_sensor, INPUT);

}

void loop() {
  i = analogRead(Current_sensor);
  Serial.println('c' + String(i));
}
