
unsigned int OUTPUT_PORT = 13;
unsigned int INPUT_PORT = 8;

unsigned int work_time = 0;
unsigned int sleep_time = 0;

// get time arguments
void get_args()
{
  while (true)
  {
    if (Serial.available() > 0)
    {
      work_time = Serial.parseInt();
      sleep_time = Serial.parseInt();
      unsigned int check_byte = (work_time + sleep_time) % 256;
      Serial.write(check_byte);
      break;
    }
  }
}

// the setup routine runs once when you press reset:
void setup()
{
  Serial.begin(38400);
  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(OUTPUT_PORT, OUTPUT);
  pinMode(INPUT_PORT, INPUT);
  get_args();
}

void _delay(unsigned int micro_seconds)
{
  if (micro_seconds < 16383)
  {
    delayMicroseconds(micro_seconds);
  }
  else
  {
    delay(micro_seconds / 1000);
  }
}

// the loop routine runs over and over again forever:
void loop()
{
  if (digitalRead(INPUT_PORT) == HIGH)
  {
    // work
    digitalWrite(OUTPUT_PORT, HIGH);
    _delay(work_time);

    // sleep
    digitalWrite(OUTPUT_PORT, LOW);
    _delay(sleep_time);
  }
}
