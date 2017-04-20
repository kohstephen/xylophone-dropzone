// author: Sophia Dolan

#include <Stepper.h>

const int stepsPerRevolution = 48; //7.5 deg per step
const int stepsRelease = 10; //more accurately, 360/5/7.5=9.6
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);
 
void setup() {
  myStepper.setSpeed(60); //60 rpm when stepping
  Serial.begin(9600); // initialize the serial port:
}

void loop() {
  String input;
  
  if (Serial.available() > 0) 
    input = Serial.readString(); // read the incoming String:
  if(input=="step"){
    Serial.println("Releasing ball");
    myStepper.step(stepsRelease);
    delay(250); //pause 0.25 seconds
  }

}
