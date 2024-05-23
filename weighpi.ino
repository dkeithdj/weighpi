#include <HX711.h>
#include <ArduinoJson.h>

#define TRIG_PIN1 2
#define ECHO_PIN1 3
#define TRIG_PIN2 13
#define ECHO_PIN2 12
#define WEIGHT_DOUT_PIN A1
#define WEIGHT_SCK_PIN A0

// Initialize ultrasonic sensors
long duration1, duration2;
float distance1, distance2;

// Initialize weight sensor
HX711 scale;
// const int calibration_factor = -16050; // adjust this according to your load cell
const int calibration_factor = -105; // adjust this according to your load cell

float totalWeight = 0.0;
int numReadings = 0;
const int NUM_READINGS_FOR_AVERAGE = 500; // 5 seconds with 100 ms delay


void setup() {
  Serial.begin(9600);
  while (!Serial) { ; } // Wait for Serial to be ready

  pinMode(TRIG_PIN1, OUTPUT);
  pinMode(ECHO_PIN1, INPUT);
  pinMode(TRIG_PIN2, OUTPUT);
  pinMode(ECHO_PIN2, INPUT);
  
  scale.begin(WEIGHT_DOUT_PIN, WEIGHT_SCK_PIN);

  scale.set_scale(calibration_factor);
  scale.tare();
}

void loop() {

  // Read ultrasonic sensor 1
  digitalWrite(TRIG_PIN1, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN1, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN1, LOW);
  duration1 = pulseIn(ECHO_PIN1, HIGH);
  distance1 = duration1 * 0.034 / 2;
  
  // Read ultrasonic sensor 2
  digitalWrite(TRIG_PIN2, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN2, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN2, LOW);
  duration2 = pulseIn(ECHO_PIN2, HIGH);
  distance2 = duration2 * 0.034 / 2;
  
  // Read weight sensor
  int weight = round(scale.get_units(10));

  // Calculate the difference from the previous weight
  
  // Prepare JSON document
  StaticJsonDocument<200> doc;
  doc["sensor_front"] = distance1;
  doc["sensor_rear"] = distance2;
  doc["weight"] = weight;

  // Check conditions for weight calculation
  if (distance1 > 12 && distance2 > 12 && weight > 10) { // Adjust distance threshold as needed
    doc["hasVehicle"] = true;
  } else {
    doc["hasVehicle"] = false;
  }

  // Serialize JSON and print
  String jsonString;
  serializeJson(doc, jsonString);
  Serial.println(jsonString);

  // Update the previous weight

  delay(300); // Adjust delay as needed
}
