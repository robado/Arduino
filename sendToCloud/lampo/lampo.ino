int sensorPin = 0;

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  //getting the voltage reading from the temperature sensor
  int reading = analogRead(sensorPin);
  //int oldReading = 0;


  float voltage = reading * 5.0;
  voltage /= 1024.0;
  // now print out the temperature
  float temperatureC = (voltage - 0.5) * 100 ;

  if (temperatureC < 42 && temperatureC > 10 ) {
    Serial.print("GET http://api.botbook.com/add/wqNvzOr0Df4/?x=");
    Serial.println(temperatureC);
    delay(10000);
  }
}
