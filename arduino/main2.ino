#include <Wire.h>

#define SLAVE_ADDRESS 0x12
int dataReceived = 0;

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


//From bildr article: http://bildr.org/2012/08/rotary-encoder-arduino/

//these pins can not be changed 2/3 are special pins
int encoderPin1 = 2;
int encoderPin2 = 3;
int encoderSwitchPin = 4; //push button switch

volatile int lastEncoded = 0;
volatile long encoderValue = 0;

long lastencoderValue = 0;

int lastMSB = 0;
int lastLSB = 0;


volatile int bigvalue = 0;

void setup() {
  Serial.begin (9600);

  Wire.begin(SLAVE_ADDRESS);

  pinMode(encoderPin1, INPUT); 
  pinMode(encoderPin2, INPUT);

  pinMode(encoderSwitchPin, INPUT);


  digitalWrite(encoderPin1, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin2, HIGH); //turn pullup resistor on

  digitalWrite(encoderSwitchPin, HIGH); //turn pullup resistor on


  //call updateEncoder() when any high/low changed seen
  //on interrupt 0 (pin 2), or interrupt 1 (pin 3) 
  attachInterrupt(0, updateEncoder, CHANGE); 
  attachInterrupt(1, updateEncoder, CHANGE);
  
  pixels.begin(); // This initializes the NeoPixel library.
  pixels.show(); // Initialize all pixels to 'off'


}

void loop(){ 

  delay(100);

  //Wire.onReceive(receiveData);
  //Wire.onRequest(rotary);
  Wire.onReceive(receiveData);
  //Wire.onRequest(rotary);
  //delay(1000); //just here to slow down the output, and show it will work  even during a delay
}


void updateEncoder(){
  int MSB = digitalRead(encoderPin1); //MSB = most significant bit
  int LSB = digitalRead(encoderPin2); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncoded << 2) | encoded; //adding it to the previous encoded value

  //if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValue ++;
  //if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValue --;
  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValue --;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValue ++;

  //if(lastEncoded == encoded) Serial.println("boom");

  lastEncoded = encoded; //store this value for next time
}

// callback for received data
void receiveData(int byteCount){
  while(Wire.available()) {
    dataReceived = Wire.read();
    Serial.print("data received: ");
    Serial.println(dataReceived);
    if(dataReceived==6){
      blinkMyLed();
      }
    }
  }

  
void sendData(){
    int envoi = dataReceived + 1;
    Wire.write(envoi);
}

void rotary(){

  //Do stuff here
  if(digitalRead(encoderSwitchPin)){
    //button is not being pushed
  }else{
    //button is being pushed
    Serial.println("push");
//    for(int i=0;i<3;i++){
//        pixels.setPixelColor(0, pixels.Color(0, 0, 255)); //blue
//        pixels.setPixelColor(1, pixels.Color(0, 0, 255)); //blue
//        pixels.show();
//        delay(delayval);
//        pixels.setPixelColor(0, pixels.Color(255, 0, 0)); //red
//        pixels.setPixelColor(1, pixels.Color(255, 0, 0)); //red
//        pixels.show();
//        delay(delayval);
//        pixels.setPixelColor(0, pixels.Color(0, 255, 0)); //green
//        pixels.setPixelColor(1, pixels.Color(0, 255, 0)); //green
//        pixels.show();
//        delay(delayval);
//        pixels.setPixelColor(0, pixels.Color(255, 255, 0)); //yellow
//        pixels.setPixelColor(1, pixels.Color(255, 255, 0)); //yellow
//        pixels.show();
//        delay(delayval);
//        }

    for(int i=0;i<5;i++){
        pixels.setPixelColor(0, pixels.Color(255, 0, 0)); //yellow
        pixels.setPixelColor(1, pixels.Color(0, 0, 0)); //yellow
        pixels.show();
        delay(delayval*4);
        pixels.setPixelColor(0, pixels.Color(0, 0, 0)); //yellow
        pixels.setPixelColor(1, pixels.Color(255, 0, 0)); //yellow
        pixels.show();
        delay(delayval*4);
        pixels.setPixelColor(0, pixels.Color(255, 0, 255)); //violet
        pixels.setPixelColor(1, pixels.Color(0, 0, 0)); //yellow
        pixels.show();
        delay(delayval*4);
        pixels.setPixelColor(0, pixels.Color(0, 0, 0)); //yellow
        pixels.setPixelColor(1, pixels.Color(255, 0, 255)); //violet
        pixels.show();
        delay(delayval*4);
        }
    
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.setPixelColor(1, pixels.Color(0, 0, 0));
    pixels.show();



    
  }

  
  if(encoderValue>=bigvalue){
    //Serial.println(encoderValue);
    bigvalue=encoderValue;
  }
  
 
  if(encoderValue < 2 and bigvalue>9){
    Serial.println(bigvalue);

    if(bigvalue>9 and bigvalue<15){
       pixels.setPixelColor(0, pixels.Color(0, 0, 255)); //blue
       pixels.setPixelColor(1, pixels.Color(0, 0, 255)); //blue
       pixels.show();
       delay(delayval*50);
       Serial.println("CHOIX 1");
        int envoi = 1;
        Wire.write(envoi);
    }

    if(bigvalue>=15 and bigvalue<25){
       pixels.setPixelColor(0, pixels.Color(255, 255, 0)); //yellow
       pixels.setPixelColor(1, pixels.Color(255, 255, 0)); //yellow
       pixels.show();
       delay(delayval*50);
       Serial.println("CHOIX 2");
    }

    if(bigvalue>=25 and bigvalue<32){
       pixels.setPixelColor(0, pixels.Color(0, 255, 0)); //green
       pixels.setPixelColor(1, pixels.Color(0, 255, 0)); //green
       pixels.show();
       delay(delayval*50);
       Serial.println("CHOIX 3");
    }

    if(bigvalue>=32 and bigvalue<42){
       pixels.setPixelColor(0, pixels.Color(255, 0, 0)); //red
       pixels.setPixelColor(1, pixels.Color(255, 0, 0)); //red
       pixels.show();
       delay(delayval*50);
       Serial.println("CHOIX 4");
    }

    if(bigvalue>=42 and bigvalue<51){
       pixels.setPixelColor(0, pixels.Color(255, 0, 255)); //violet
       pixels.setPixelColor(1, pixels.Color(255, 0, 255)); //violet
       pixels.show();
       delay(delayval*50);
       Serial.println("CHOIX 5");
    }

    if(bigvalue>=51 and bigvalue<62){
      for(int i=0;i<5;i++){
         pixels.setPixelColor(0, pixels.Color(255, 0, 255)); //violet
         pixels.setPixelColor(1, pixels.Color(255, 0, 255)); //violet
         pixels.show();
         delay(delayval*50);
         pixels.setPixelColor(0, pixels.Color(255, 255, 255)); //white
         pixels.setPixelColor(1, pixels.Color(255, 255, 255)); //white
         pixels.show();
         delay(delayval*50);
      }
       Serial.println("CHOIX 6");
    }
    
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.setPixelColor(1, pixels.Color(0, 0, 0));
    pixels.show();
    bigvalue = 0;
  }
}

void blinkMyLed(){

    for(int i=0;i<5000;i++){
        Wire.write(envoi);
        pixels.setPixelColor(0, pixels.Color(255, 0, 0)); //yellow
        pixels.setPixelColor(1, pixels.Color(0, 0, 0)); //yellow
        pixels.show();
        //delay(delayval*4);
        pixels.setPixelColor(0, pixels.Color(0, 0, 0)); //yellow
        pixels.setPixelColor(1, pixels.Color(255, 0, 0)); //yellow
        pixels.show();
        //delay(delayval*4);
        pixels.setPixelColor(0, pixels.Color(255, 0, 255)); //violet
        pixels.setPixelColor(1, pixels.Color(0, 0, 0)); //yellow
        pixels.show();
        //delay(delayval*4);
        pixels.setPixelColor(0, pixels.Color(0, 0, 0)); //yellow
        pixels.setPixelColor(1, pixels.Color(255, 0, 255)); //violet
        pixels.show();
        //delay(delayval*4);
        }
    
    pixels.setPixelColor(0, pixels.Color(0, 0, 0));
    pixels.setPixelColor(1, pixels.Color(0, 0, 0));
    pixels.show();


}
