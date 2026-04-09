
// servo code from earlier in semester!!!

// #include <Servo.h>
// Servo ssm;
int angle = 0;


void setup() {
  // put your setup code here, to run once:
  ssm.attach(9);
  ssm.write(90);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  for(angle = 10; angle < 180; angle++){
    setServo(angle);
    delay(20);
    //ssm.write(angle+10);
    //delay(20);


  }

  for(angle = 180; angle > 10; angle--){
    setServo(angle);
    delay(20);
   //   ssm.write(angle-10);
    //delay(20);
  }

}

void setServo(int s){
  if (s >= 0 && s < 90){
    ssm.write(s);
  }
  else {}
}

