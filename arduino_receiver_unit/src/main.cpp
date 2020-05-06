#include <Arduino.h>
// actual frequency of the RC module
#define MEASURED_FREQ 54.4899738
#define WANTED_FREQ 50

// trim of the channel like on the RC remote (RC trim can be 0) in us
#define TRIM_CH1 -47
#define TRIM_CH2 -21

#define CHANNEL_MASK 0x8000
#define PWM_MASK 0x7FFF
#define CONFIG_RUNNING 0x0001

volatile uint16_t pwm_valueCh1 = 0;
volatile uint16_t pwm_valueCh2 = 0;
volatile uint16_t prev_timeCh1 = 0;
volatile uint16_t prev_timeCh2 = 0;
volatile uint16_t new_timeCh1 = 0;
volatile uint16_t new_timeCh2 = 0;

void fallingCh2();
void fallingCh1();

uint16_t frequency_correction(uint16_t pwm) {
  return (pwm*MEASURED_FREQ)/WANTED_FREQ;
}

uint16_t trim(byte ch, uint16_t pwm) {
  switch (ch) {
    case 1:
      return pwm+TRIM_CH1;
      break;
    case 2:
      return pwm+TRIM_CH2;
      break;
    default:
      return pwm;
      break;
  }
}

void prepareAndSend() {
  pwm_valueCh2 = new_timeCh2 - prev_timeCh2;
  pwm_valueCh1 = new_timeCh1 - prev_timeCh1;

  pwm_valueCh2 = frequency_correction(pwm_valueCh2);
  pwm_valueCh2 = trim(2, pwm_valueCh2);
  pwm_valueCh1 = frequency_correction(pwm_valueCh1);
  pwm_valueCh1 = trim(1, pwm_valueCh1);

#ifdef DEBUG
  Serial.println(pwm_valueCh1);
  Serial.println(pwm_valueCh2);
#else
  uint16_t payloadCh1 = pwm_valueCh1 & PWM_MASK;
  Serial.println(payloadCh1);
  uint16_t payloadCh2 = pwm_valueCh2 & PWM_MASK;
  payloadCh2 = payloadCh2 | CHANNEL_MASK;
  Serial.println(payloadCh2);
#endif
}

void risingCh2() {
  attachInterrupt(1, fallingCh2, FALLING);
  prev_timeCh2 = micros();
}

void fallingCh2() {
  attachInterrupt(1, risingCh2, RISING);
  new_timeCh2 = micros();
  // this will be done here due to timing
  // falling edge ch2 is the last interrupt within a 50Hz period
  prepareAndSend();
}

void risingCh1() {
  attachInterrupt(0, fallingCh1, FALLING);
  prev_timeCh1 = micros();
}

void fallingCh1() {
  attachInterrupt(0, risingCh1, RISING);
  new_timeCh1 = micros();
}

void setup() {
  Serial.begin(115200);
  attachInterrupt(0, risingCh1, RISING);
  attachInterrupt(1, risingCh2, RISING);
}

void loop() {}
