#include <PowerFunctions.h>
#include <SoftwareSerial.h>

PowerFunctions pf(12, 0);
SoftwareSerial soft(3, 4);
int incomingByte = 0;
int last = 0;
#define echoPin 6 
#define trigPin 5
double d=0;

// defines variables
long duration; // variable for the duration of sound wave travel
double distance; // variable for the distance measurement


void setup() {
  // put your setup code here, to run once:
  soft.begin(9600);
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
}

void loop() {
  d=measureD();
  last = incomingByte;
  if (last=='m'){
    incomingByte='0';
  }
  if (soft.available() > 0) {
    // read the (incoming byte:
    incomingByte = soft.read();
    Serial.write(incomingByte);
  

  }
  if (incomingByte == 'z' && d>40) {
    forward();
  } else if (incomingByte == 's') {
    backward();
  } else if (incomingByte == 'q') {
    fastTurnLeft();
  } else if (incomingByte == 'd') {
    fastTurnRight();
  } else if (incomingByte == 'L') {
    fastTurnLeft();
  } else if (incomingByte == 'R') {
    fastTurnRight();
  } else if (incomingByte == 'a' && last != 'a') {
    interrupt();
  } else if (incomingByte == 'm' && last != 'm') {
    soft.print(measureD());
    soft.print("\n");
  }
  if(d<35 && incomingByte=='z'){
    interrupt();
  }
  
}


double measureD(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  return distance;
//  return 1000;
}

void forward() {
  pf.combo_pwm(PWM_REV7, PWM_FWD7);
}

void backward() {
  pf.combo_pwm(PWM_FWD7, PWM_REV7);
}

void turnRight() {
  pf.combo_pwm(PWM_REV7, PWM_BRK);
}

void turnLeft() {
  pf.combo_pwm(PWM_BRK, PWM_FWD7);
}

void fastTurnRight() {
  pf.combo_pwm(PWM_REV7, PWM_REV7);
}

void fastTurnLeft() {
  pf.combo_pwm(PWM_FWD7, PWM_FWD7);
}

void interrupt() {
  pf.combo_pwm(PWM_BRK, PWM_BRK);
  delay(30);
  pf.combo_pwm(PWM_FLT, PWM_FLT);
}
