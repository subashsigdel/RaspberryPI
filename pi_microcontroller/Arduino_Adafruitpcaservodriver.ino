#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca1 = Adafruit_PWMServoDriver(0x40);  // PCA 1 (pins 1–16)
Adafruit_PWMServoDriver pca2 = Adafruit_PWMServoDriver(0x41);  // PCA 2 (pins 17–32)

#define TOTAL_PINS 32

// Convert angle (0–180) to pulse length (150–600)
int angleToPulse(int angle) {
  return map(angle, 0, 180, 150, 600);
}

// Set angle in degrees (0–180) to logical pin 1–32
void setAngleDegrees(int pin, int angle) {
  int pulse = angleToPulse(angle);

  if (pin >= 1 && pin <= 16) {
    pca1.setPWM(pin - 1, 0, pulse);
  } else if (pin >= 17 && pin <= 32) {
    pca2.setPWM(pin - 17, 0, pulse);
  } else {
    Serial.println(F("Invalid pin number."));
  }
}

void setup() {
  Serial.begin(9600);
  Wire.begin();

  pca1.begin();
  pca2.begin();
  pca1.setPWMFreq(50);
  pca2.setPWMFreq(50);

  Serial.println(F("\n🧪 Servo Pin Controller Ready (1–32)"));
  Serial.println(F("Type: <pin>, <pin angle>, all, all <angle>, or exit"));
}

void loop() {
  static String input = "";

  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      input.trim();

      if (input.equalsIgnoreCase("exit")) {
        Serial.println(F("Exiting."));
        while (1); // Stop execution
      }

      else if (input.startsWith("all")) {
        int angle = 90; // Default
        int spaceIndex = input.indexOf(' ');
        if (spaceIndex > 0) {
          angle = input.substring(spaceIndex + 1).toInt();
        }

        angle = constrain(angle, 0, 180);
        Serial.print(F("Setting ALL pins to "));
        Serial.print(angle);
        Serial.println(F("°"));

        for (int i = 1; i <= TOTAL_PINS; i++) {
          setAngleDegrees(i, angle);
          delay(100);  // Delay to prevent current spike
        }
      }

      else if (input.length() > 0) {
        int spaceIndex = input.indexOf(' ');
        int pin = 0;
        int angle = 90;  // Default

        if (spaceIndex > 0) {
          pin = input.substring(0, spaceIndex).toInt();
          angle = input.substring(spaceIndex + 1).toInt();
        } else {
          pin = input.toInt();
        }

        if (pin >= 1 && pin <= TOTAL_PINS && angle >= 0 && angle <= 180) {
          Serial.print(F("Setting PIN "));
          Serial.print(pin);
          Serial.print(F(" to "));
          Serial.print(angle);
          Serial.println(F("°"));

          setAngleDegrees(pin, angle);
        } else {
          Serial.println(F("Usage: <pin 1–32> <angle 0–180>"));
        }
      }

      input = ""; // Reset
      Serial.println(F("\nEnter next command:"));
    } else {
      input += c;
    }
  }
}
