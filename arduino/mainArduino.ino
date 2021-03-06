#include <Wire.h>
#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

#define SLAVE_ADDRESS 0x12
int dataReceived = 0;

int pos = 40;    // variable to store the servo position

// Based on NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license 
#include <Adafruit_NeoPixel.h>
// Which pin on the Digispark is connected to the DigiLED?
#define PIN            8
// How many DigiLEDs are attached to the Digispark?
#define NUMPIXELS      2
// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// For the WS2812B type through hole LED used by the DigiLED,  NEO_RGB + NEO_KHZ800 is the correct data format
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_RGB + NEO_KHZ800);
int delayval = 10; // delay for half a second
int bigvalue = 0;
const char* seqLed[]={"x","gxyxgxyxg","rxyxrxyxrxy","yxoxr","r","g","yxoxr","w","rxgxbxrxgxb"};

void setup() {

  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(180);
  
  Serial.begin (9600);

  Wire.begin(SLAVE_ADDRESS);
  
  pixels.begin(); // This initializes the NeoPixel library.
  pixels.show(); // Initialize all pixels to 'off'

}

void loop(){ 

  delay(100);
  Wire.onReceive(receiveData);
  //Wire.onRequest(rotary);
  //delay(1000); //just here to slow down the output, and show it will work  even during a delay
}



// callback for received data
void receiveData(int byteCount){
  while(Wire.available()) {
    dataReceived = Wire.read();
    Serial.print("data received: ");
    Serial.println(dataReceived);
    if(dataReceived==1){
      blinkMyLed(1,5);
      }
    else if(dataReceived==2){
      blinkMyLed(2,5);
      }
    else if(dataReceived==3){
      blinkMyLed(3,5);
      }
    else if(dataReceived==4){
      for(int i=0;i<5;i++){
        myLedOn('r');
        myservo.write(120);
        delay(200);
        myLedOn('y');
        myservo.write(180);
        delay(200);
        }
      myLedOn('x');
      }
    else if(dataReceived==5){
      blinkMyLed(5,5);
      }
    else if(dataReceived==6){
      blinkMyLed(6,5);
      }
    else if(dataReceived==7){
      blinkMyLed(7,5);
      }
    else if(dataReceived==8){
      blinkMyLed(8,10);
      }
    else if(dataReceived==11){
      myLedOn('g');
      //delay(2000);
      myservo.write(100);
      delay(1000);
      myservo.write(180);
      delay(1000);
      myservo.write(100);
      delay(1000);
      myservo.write(180);
      myLedOn('x');
      }
    }
  }

void blinkMyLed(int choice, int factorDelay){
      for(int a=0;a<10;a++){
          for(int i=0;i<sizeof(seqLed[choice])+1;i++){
              myLedOn(seqLed[choice][i]);
              delay(delayval*factorDelay);
              }
          }
      myLedOn('x');
}

void myLedOn(char color){
    for(int i=0;i<NUMPIXELS;i++){
        switch (color) {
            case 'r'://red
              pixels.setPixelColor(i, pixels.Color(255, 0, 0));
              break;
            case 'g'://green
              pixels.setPixelColor(i, pixels.Color(0, 255, 0)); 
              break;
            case 'b'://blue
              pixels.setPixelColor(i, pixels.Color(0, 0, 255)); 
              break;
            case 'y'://yellow
              pixels.setPixelColor(i, pixels.Color(255, 255, 0));
              break;
            case 'v'://violet
              pixels.setPixelColor(i, pixels.Color(255, 0, 255));
              break;
            case 'w'://white
              pixels.setPixelColor(i, pixels.Color(255, 255, 255));
              break;
            case 'o'://orange
              pixels.setPixelColor(i, pixels.Color(255, 122, 0));
              break;
            case 'x'://off
              pixels.setPixelColor(i, pixels.Color(0, 0, 0));
              break;
            default: 
              pixels.setPixelColor(i, pixels.Color(0, 0, 0));
            break;
          }
    }
    pixels.show();
}





