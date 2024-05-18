#include <HX711.h>
#include <ArduinoJson.h>

#define TRIG_PIN1 2
#define ECHO_PIN1 3
#define TRIG_PIN2 4
#define ECHO_PIN2 5
#define WEIGHT_DOUT_PIN A1
#define WEIGHT_SCK_PIN A0

// Initialize ultrasonic sensors
long duration1, duration2;
float distance1, distance2;

// Initialize weight sensor
HX711 scale;
const int calibration_factor = -7050; // adjust this according to your load cell
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
  

}

void loop() {
    JsonDocument doc;

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
  float weight = scale.get_units(10);
  // Serial.print("Weight: ");
  // Serial.println(weight);

  // Serial.print("US1: ");
  // Serial.println(distance1);

  // Serial.print("US2: ");
  // Serial.println(distance2);

  doc["sensor_front"] = distance1;
  doc["sensor_rear"] = distance2;
  doc["weight"] = weight;

  // Check conditions for weight calculation
  if (distance1 > 20 && distance2 > 20 && weight > 80) { // Adjust distance threshold as needed
    // Serial.println(weight);
    // totalWeight += weight;
    // numReadings++;
    // if (numReadings >= NUM_READINGS_FOR_AVERAGE) {
      // float averageWeight = totalWeight / numReadings;
      // Send average weight to Raspberry Pi
      // Serial.print("W,");
      // Serial.println(weight);
      doc["hasVehicle"] = true;
      // Serial.println(",");
      // totalWeight = 0.0;
      // numReadings = 0;
    // }
  } else {
      doc["hasVehicle"] = false;
    // totalWeight = 0.0; // Reset total weight if either ultrasonic sensor is blocked
    // numReadings = 0; // Reset number of readings
  }
  String jsonString;
  serializeJson(doc,jsonString);
  Serial.println(jsonString);
  
  delay(300); // Adjust delay as needed
}

