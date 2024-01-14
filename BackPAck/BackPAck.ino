/* This example Arduino Sketch controls the complete rotation of
 *  SG995 Servo motor by using its PWM and Pulse width modulation technique
 */

#include "Servo.h" // include servo library to use its related functions
#define Servo_PWM 7 // A descriptive name for D6 pin of Arduino to provide PWM signal
#define LEDGreen 35
#define LEDBlue 33
#define LEDRed 31
Servo MG995_Servo;  // Define an instance of of Servo with the name of "MG995_Servo"
bool blink = false;

void setup() {
  Serial1.begin(9600);
  Serial.begin(9600); // Initialize UART with 9600 Baud rate
  MG995_Servo.attach(Servo_PWM);  // Connect D6 of Arduino with PWM signal pin of servo motor
  pinMode(LEDGreen, OUTPUT);
  pinMode(LEDBlue, OUTPUT);
  pinMode(LEDRed, OUTPUT);
  digitalWrite(LEDGreen, LOW);
  digitalWrite(LEDBlue, LOW);
  digitalWrite(LEDRed, LOW);
}

unsigned long previousMillis = 0; // Variable to store the previous time
const unsigned long interval = 1000; // Blink interval in milliseconds

void loop() {
  unsigned long currentMillis = millis(); // Get the current time

  if (currentMillis - previousMillis >= interval) { // Check if the interval has passed
    previousMillis = currentMillis; // Update the previous time

    // Toggle the LED state
    if (blink) {
      digitalWrite(LEDBlue, !digitalRead(LEDBlue));
    }
  }

  if (Serial1.available() > 0) // Check if any data is available on UART
  {
    char angle = Serial1.read(); // Read the data and convert it into integer
    if (angle == 'o') {
      digitalWrite(LEDRed, HIGH);
      MG995_Servo.write(135); // Rotate the servo motor to the specified angle
      Serial.println(135); // Print the angle on serial monitor
      digitalWrite(LEDRed, LOW);
      blink = true;
    } else if (angle == 'c') {
      MG995_Servo.write(0); // Rotate the servo motor to the specified angle
      Serial.println(0); // Print the angle on serial monitor
      blink = false;
    }
  }
}