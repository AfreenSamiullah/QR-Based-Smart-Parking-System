#include <CheapStepper.h>
#include <Servo.h>

Servo servo1;
#define ir 6         // IR sensor pin

CheapStepper stepper(8, 9, 10, 11);  // Stepper motor pins

bool waitingForPython = false;

void setup() {
  Serial.begin(9600);
  pinMode(ir, INPUT);
  servo1.attach(7);
  stepper.setRpm(17);
  delay(1000);  // Give small break
  servo1.write(0);
  delay(1000);  // Give small break
  servo1.write(130);  // Start position
  delay(1000);  // Give small break
  stepper.moveDegreesCCW(50);
  delay(1000);  // Give small break
  stepper.moveDegreesCW(50);
  delay(1000);
}

void loop() {
  int irValue = digitalRead(ir);

  if (irValue == 0 && !waitingForPython) {  // Object detected
    Serial.println("DETECT");               // Notify Python
    waitingForPython = true;                // Prevent resending until processed
    delay(1000);  // debounce delay
  }

  // Wait for Python's classification
  if (Serial.available() > 0) {
    String classification = Serial.readStringUntil('\n');
    classification.trim();

    Serial.print("Received classification: ");
    Serial.println(classification);

    if (classification == "metal") {
      stepper.moveDegreesCW(100);  // Adjust degrees if needed
      delay(1000);
      dropItem();
      stepper.moveDegreesCCW(100);
    } else if (classification == "organic") {
      stepper.moveDegreesCCW(130);  // Adjust degrees if needed
      delay(1000);
      dropItem();
      stepper.moveDegreesCW(130);
    } else if (classification == "plastic") {
      dropItem();
    }

    Serial.println("OK");  // Notify Python that action is done
    waitingForPython = false;  // Ready for next detection
  }
}

void dropItem() {
  servo1.write(0);  // Open flap
  delay(2000);
  servo1.write(130);    // Close flap
  delay(1000);
}
