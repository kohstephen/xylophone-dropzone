int latchPin = 8;
int clockPin = 12;
int dataPin = 11;
unsigned long currentTime;
int inByte;

void setup() {
  Serial.begin(9600); // set the baud rate
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);

  inByte = ' ';
  
  digitalWrite(latchPin, LOW);
  while(Serial.available() <= 0){};
  inByte = Serial.read();
  shiftOut(dataPin, clockPin, MSBFIRST, inByte);
  
}
void loop() {

  currentTime = millis();
  digitalWrite(latchPin, HIGH);
  Serial.println(inByte); // send the data back in a new line so that it is not all one long line
  digitalWrite(latchPin, LOW);
  while(Serial.available() <= 0){};
  inByte = Serial.read();
  shiftOut(dataPin, clockPin, MSBFIRST, inByte);
  if(millis() - currentTime < 10){
    delay(10 - (millis()-currentTime));
  }
  
  
}
