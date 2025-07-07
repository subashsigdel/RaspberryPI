#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca1 = Adafruit_PWMServoDriver(0x40);  // Pins 1–16
Adafruit_PWMServoDriver pca2 = Adafruit_PWMServoDriver(0x41);  // Pins 17–32

// Angle to PWM pulse (microseconds)
int angleToPulse(int angle) {
  return map(angle, 0, 180, 150, 600);
}

// --- Servo Pin Map ---
const int Rthumb  = 23;
const int Rindex  = 24;
const int Rmiddle = 26;
const int Rring   = 27;
const int Rpinky  = 28;
const int rWrist  = 25;

const int Lthumb  = 10;
const int Lindex  = 9;
const int Lmiddle = 8;
const int Lring   = 7;
const int Lpinky  = 6;
const int lWrist  = 5;

// Group pins for convenience
int rightHand[] = {Rthumb, Rindex, Rmiddle, Rring, Rpinky, rWrist};
int leftHand[]  = {Lthumb, Lindex, Lmiddle, Lring, Lpinky, lWrist};

// Set angle to any of the 32 logical pins
void setAngleDegrees(int pin, int angle) {
  int pulse = angleToPulse(angle);
  if (pin >= 1 && pin <= 16)
    pca1.setPWM(pin - 1, 0, pulse);
  else if (pin >= 17 && pin <= 32)
    pca2.setPWM(pin - 17, 0, pulse);
  else
    Serial.println(F("Invalid pin number."));
}

// Set multiple pins to an angle
void setPins(int pins[], int len, int angle) {
  for (int i = 0; i < len; i++) {
    setAngleDegrees(pins[i], angle);
  }
}

// --- Gestures ---
void openHands() {
  setPins(rightHand, 5, 0);
  setPins(leftHand, 5, 0);
}

void closeHands() {
  setPins(rightHand, 5, 180);
  setPins(leftHand, 5, 180);
}

void thumbsUp() {
  setAngleDegrees(Rthumb, 0);
  setPins(rightHand + 1, 4, 180);  // close other right fingers
  setAngleDegrees(Lthumb, 0);
  setPins(leftHand + 1, 4, 180);
}

void thumbsDown() {
  setAngleDegrees(Rthumb, 180);
  setPins(rightHand + 1, 4, 180);
  setAngleDegrees(Lthumb, 180);
  setPins(leftHand + 1, 4, 180);
}

void peaceSign() {
  setAngleDegrees(Rindex, 0);
  setAngleDegrees(Rmiddle, 0);
  setAngleDegrees(Rthumb, 180);
  setAngleDegrees(Rring, 180);
  setAngleDegrees(Rpinky, 180);
}

void fist() {
  closeHands();
}

void resetWrist() {
  setAngleDegrees(rWrist, 90);
  setAngleDegrees(lWrist, 90);
}

void setup() {
  Serial.begin(9600);
  Wire.begin();
  pca1.begin(); pca2.begin();
  pca1.setPWMFreq(50);
  pca2.setPWMFreq(50);

  Serial.println(F("\nFinger Controller Ready"));
  Serial.println(F("Commands: open, close, thumbsup, thumbsdown, peace, fist, reset"));
}

void loop() {
  static String input = "";

  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      input.trim();

      if (input.equalsIgnoreCase("open")) {
        openHands();
        Serial.println(F("Hands opened"));
      } else if (input.equalsIgnoreCase("close")) {
        closeHands();
        Serial.println(F("Hands closed"));
      } else if (input.equalsIgnoreCase("thumbsup")) {
        thumbsUp();
        Serial.println(F("Thumbs up"));
      } else if (input.equalsIgnoreCase("thumbsdown")) {
        thumbsDown();
        Serial.println(F("Thumbs down"));
      } else if (input.equalsIgnoreCase("peace")) {
        peaceSign();
        Serial.println(F("Peace sign"));
      } else if (input.equalsIgnoreCase("fist")) {
        fist();
        Serial.println(F("Fist made"));
      } else if (input.equalsIgnoreCase("reset")) {
        resetWrist();
        Serial.println(F("Wrists reset to 90°"));
      } else {
        Serial.println(F("Unknown command"));
      }

      input = "";
      Serial.println(F("\nEnter next command:"));
    } else {
      input += c;
    }
  }
}
