
#include "Adafruit_VL53L0X.h"                              

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

float maxdist = 200; // дистанция, при которой включается нагрузка

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  while (! Serial) {
    delay(1);
  }
  
  Serial.println("Adafruit VL53L0X");
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }
  Serial.println(F("VL53L0X API\n\n")); 
}

void loop() {
  
  VL53L0X_RangingMeasurementData_t measure;
  
  // Serial.print("Reading a measurement... ");
  lox.rangingTest(&measure, false);

  int dist = measure.RangeMilliMeter;
  
  if (measure.RangeStatus != 4)
    if (dist < maxdist) {
      Serial.println("LED ON");
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else {  
      Serial.print("Distance (mm): "); Serial.println(dist);
      digitalWrite(LED_BUILTIN, LOW);
    }
  else {
    Serial.println("out of range");
    digitalWrite(LED_BUILTIN, LOW);
  }
  delay(100);
}
