//Parameters
const int micPin   = A0;

//Variables
//int micVal  = 0;

void setup() {
  //Init Serial USB
  Serial.begin(9600);
  Serial.println(F("Initialize System"));
  //Init Microphone
  pinMode(micPin, INPUT);
}

void loop() {
  readMicrophone();
}

void readMicrophone( ) { /* function readMicrophone */
  ////Test routine for Microphone
  //micVal = analogRead(micPin);
  bool too_loud = digitalRead(2);
  Serial.println(too_loud);
  delay(1000);
}
