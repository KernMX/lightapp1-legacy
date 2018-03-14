/*
  __  __         ______               _____       _____ _ 
 |  \/  |       |  ____|             |_   _|     |  __ (_)
 | \  / |_   _  | |__ __ _  ___ ___    | |  ___  | |__) | 
 | |\/| | | | | |  __/ _` |/ __/ _ \   | | / __| |  ___/ |
 | |  | | |_| | | | | (_| | (_|  __/  _| |_\__ \ | |   | |
 |_|  |_|\__, | |_|  \__,_|\___\___| |_____|___/ |_|   |_|
          __/ |                                           
         |___/                                           
 */
#include <FS.h>                   //this needs to be first, or it all crashes and burns...

#include "ws2812_i2s.h"
#include "FastLED.h"
#include <ESP8266WiFi.h>          //https://github.com/esp8266/Arduino
#include <WiFiUdp.h>

#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>          //https://github.com/tzapu/WiFiManager

/************ WIFI and UDP Packet Information (CHANGE THESE FOR YOUR SETUP) ******************/
#define BUFFER_LEN 1024 //Maximum number of packets to hold in the buffer. Don't change this.
unsigned int localPort = 7777;
char packetBuffer[BUFFER_LEN];
WiFiUDP port;
uint8_t N = 0;

/********************************* LED Strip Definitions *****************************************/
#define NUM_LEDS    180
CRGB leds[NUM_LEDS];
static native::WS2812 ledstrip;
static Pixel_t pixels[NUM_LEDS];;

byte brightness = 50;
unsigned int fps = 120;

/********************************** GLOBALS for Animations ******************************/
//GENERAL
String animation;
uint8_t gHue = 0;
unsigned long previousMillis = 0; 

//CYLON and FADE
//static uint8_t hue = 0;
int LED = 0;
bool forward = true;

//FLASH
int flash_index = 0;

//VISUALIZE
bool okvis = false;
/********************************** START SETUP *****************************************/
void setup() {
    // Set to Serial Communication rate
    //delay(1000); // 1 second delay for recovery
    Serial.begin(9600);

    //WiFiManager
    //Local intialization. Once its business is done, there is no need to keep it around
    WiFiManager wifiManager;
    
    // IP must match the IP in config.py
    IPAddress _ip(192, 168, 1, 169);
    IPAddress _gw(192, 168, 1, 1);
    IPAddress _sn(255, 255, 255, 0);
    wifiManager.setSTAStaticIPConfig(_ip, _gw, _sn);

    //tries to connect to last known settings
    //if it does not connect it starts an access point with the specified name
    //here  "AutoConnectAP" with password "password"
    //and goes into a blocking loop awaiting configuration
    if (!wifiManager.autoConnect("LED Strip", "password")) {
      Serial.println("failed to connect, we should reset as see if it connects");
      delay(3000);
      ESP.reset();
      delay(5000);
    }

    //if you get here you have connected to the WiFi
    Serial.println("connected...yeey :)");
    
    
    Serial.println("local ip");
    Serial.println(WiFi.localIP());
  
    // Start listening for UDP Packets on localPort
    port.begin(localPort);
    
    ledstrip.init(NUM_LEDS);
    fill_rainbow(leds, NUM_LEDS, 0);
    update_leds();
    animation = "off";
}



/********************************** START SET ANIMATION *****************************************/
void setAnimation(char packet[BUFFER_LEN]){
    String command(packet);
    if(command == "off"){
      okvis = false;
      Serial.println("Turning Off");
      animation = "off";
      turnOff();
    }
    else if(command == "rainbow"){
        okvis = false;
        Serial.println("Rainbow Animation");
        animation = "rainbow";
        //fill_rainbow(leds, NUM_LEDS, 0);;
    }
    else if(command == "cylon"){
      okvis = false;
      turnOff();
      Serial.println("Cylon Animation");
      animation = "cylon";
    }
    else if(command.substring(0, 6) == "static"){
      okvis = false;
        Serial.println("Changing Color");
        animation = "static";

        //Split end of command string into rgb values
        String rgbvals = command.substring(7);
        String rgbArray[3];
        int arrayIndex = 0;
        for(int i = 0; i < 3; i++){
            rgbArray[i] = "";
        }
        for(int i = 0; i < rgbvals.length(); i++){
            if(rgbvals[i] == ' '){ 
                arrayIndex++;
                continue; 
            }
            rgbArray[arrayIndex] += rgbvals[i];
        }

        //show strip
        setStripColor(rgbArray[0].toInt(), rgbArray[1].toInt(), rgbArray[2].toInt());
    }
    else if(command == "stop"){
      okvis = false;
        Serial.println("Stopping");
        animation = "stop";
    }
    else if(command == "visualize"){
      okvis = false;
      turnOff();
      Serial.println("Visualizing");
      animation = "visualize";
    }
    else if(command == "flash"){
      okvis = false;
      Serial.println("Flashin");
      animation = "flash";
    }
    else if(command == "fade"){
      okvis = false;
      Serial.println("Fading");
      animation = "fade";
    }
    else if(command == "rainbowWithGlitter"){
      okvis = false;
      //Serial.println("Rainbow With Glitter");
      animation = "rainbowWithGlitter";
    }
    else if(command == "confetti"){
      okvis = false;
      //Serial.println("Confetti");
      animation = "confetti";
    }
    else if(command == "sinelon"){
      okvis = false;
      //Serial.println("Sinelon");
      animation = "sinelon";
    }
    else if(command == "bpm"){
      okvis = false;
      //Serial.println("BPM");
      animation = "bpm";
    }
    else if(command == "juggle"){
      okvis = false;
      //Serial.println("Juggle");
      animation = "juggle";
    }
    else if(command.substring(0, 10) == "brightness"){
      okvis = false;
      brightness = command.substring(11).toInt();
      update_leds();
    }
    else if(command.substring(0, 5) == "speed"){
      okvis = false;
      fps = command.substring(6).toInt();
    }
    else{
      //Serial.println(command);
    }
}



/********************************** START PLAY ANIMATION *****************************************/
void playAnimation(){
    if(animation == "cylon"){
        cylon();
    }
    else if(animation == "rainbow"){
        rainbow();
    }
    else if(animation == "fade"){
        fade();
    }
    else if(animation == "flash"){
        flash();
    }
    else if(animation == "rainbowWithGlitter"){
        rainbowWithGlitter();
    }
    else if(animation == "confetti"){
        confetti();
    }
    else if(animation == "sinelon"){
        sinelon();
    }
    else if(animation == "bpm"){
        bpm();
    }
    else if(animation == "juggle"){
        juggle();
    }
}



/********************************** START MAIN LOOP *****************************************/
void loop() {
    // Read data over socket
    int packetSize = port.parsePacket();
    
    // If packets have been received, interpret the command
    if (packetSize) {
        // Read the packet into packetBufffer
        int len = port.read(packetBuffer, BUFFER_LEN);
        if (len > 0) {
            packetBuffer[len] = 0;
        }  
        
        // Reading packets to determine which animation to play
        setAnimation(packetBuffer); 
        
        //Visualize if set
        if(animation == "visualize" && okvis){ //TODO Find a more elegant solution than okvis
            for(int i = 0; i < len; i+=4) { //TODO find a way to purge the pixels buffer or something
                packetBuffer[len] = 0;
                N = packetBuffer[i];
                //Serial.print(N);
                pixels[N].R = (uint8_t)packetBuffer[i+1];
                pixels[N].G = (uint8_t)packetBuffer[i+2];
                pixels[N].B = (uint8_t)packetBuffer[i+3];
                pixels[N + 60].R = (uint8_t)packetBuffer[i+1];
                pixels[N + 60].G = (uint8_t)packetBuffer[i+2];
                pixels[N + 60].B = (uint8_t)packetBuffer[i+3];
                pixels[N + 120].R = (uint8_t)packetBuffer[i+1];
                pixels[N + 120].G = (uint8_t)packetBuffer[i+2];
                pixels[N + 120].B = (uint8_t)packetBuffer[i+3];
            } 
            showLEDStrip();
            
        }   
        okvis = true;                
    }

    //Changes base rainbow color every N ms Depending on Animation Speed
    //EVERY_N_MILLISECONDS( 20 ) { gHue++; }
    cycleHue();
    
    //Play the animations
    playAnimation();
}



/********************************** UPDATE_LEDS BOOL  *****************************************/
//Determines if it is time to update the LED's
void update_leds(){
  for(int i=0; i<NUM_LEDS; i++){
      pixels[i].R = leds[i].r;
      pixels[i].G = leds[i].g;
      pixels[i].B = leds[i].b;
  }
  showLEDStrip();
}

void showLEDStrip(){
  for(int i=0; i<NUM_LEDS; i++){
      pixels[i].R = pixels[i].R * brightness / 100;
      pixels[i].G = pixels[i].G * brightness / 100;
      pixels[i].B = pixels[i].B * brightness / 100;
  }
  ledstrip.show(pixels);
}


/********************************** ANIMATION FUNCTIONS  *****************************************/
//CYCLE HUE
void cycleHue(){
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= 1000/fps) {
    // save the last time you changed Hue
      previousMillis = currentMillis;
      
      gHue++;
    }
}

//TURN OFF
void turnOff(){
    setStripColor(0,0,0);
}

//SETSTRIPCOLOR
void setStripColor(int red, int green, int blue){
    fill_solid(leds, NUM_LEDS, CRGB(red, green, blue));
    update_leds();
}

//CYLON
void fadeall() { for(int i = 0; i < NUM_LEDS; i++) { leds[i].nscale8(247); } }

void cylon(){
    fadeall();
    // First slide the led in one direction
      if(LED >= NUM_LEDS - 1){
          forward = false;
      }
      else if(LED <= 0){
          forward = true;
      }
      if(forward){
          LED++;
      }
      else{
          LED--;
      }
      leds[LED] = CHSV(gHue, 255, 255);
      update_leds(); 
      delay(1000/fps); 
}

//FADE
void fade(){
      for(int i=0; i < NUM_LEDS; i++){
          leds[i] = CHSV(gHue, 255, 255);    
      } 
      update_leds(); 
      delay(1000/fps); //TODO need to update color more slowly
}

//FLASH
void flash(){
      if(flash_index == 0){
          fill_solid(leds, NUM_LEDS, CRGB::Red);
          flash_index++;
      }
      else if(flash_index == 1){
          fill_solid(leds, NUM_LEDS, CRGB::Green);
          flash_index++;
      }
      else{
          fill_solid(leds, NUM_LEDS, CRGB::Blue);
          flash_index = 0;
      }
      //Serial.println("flash");  
      update_leds(); 
      delay(30000/fps);    
}

//RAINBOW
void rainbow() 
{
    // FastLED's built-in rainbow generator
    fill_rainbow( leds, NUM_LEDS, gHue, 7);
    update_leds(); 
    delay(1000/fps);
}

//RAINBOWWITHGLITTER
void rainbowWithGlitter() 
{
    // built-in FastLED rainbow, plus some random sparkly glitter
    rainbow();
    addGlitter(80);
    update_leds(); 
    delay(1000/fps);
}

void addGlitter( fract8 chanceOfGlitter) 
{
    if( random8() < chanceOfGlitter) {
      leds[ random16(NUM_LEDS) ] += CRGB::White;
    }
}

//CONFETTI
void confetti() 
{
    // random colored speckles that blink in and fade smoothly
    fadeToBlackBy( leds, NUM_LEDS, 10);
    int pos = random16(NUM_LEDS);
    leds[pos] += CHSV( gHue + random8(64), 200, 255);
    update_leds(); 
    delay(2000/fps);
}

//SINELON
void sinelon()
{
    fadeall();
    if(LED >= NUM_LEDS){
        LED = 0;
    }
    leds[LED] = CHSV(gHue, 255, 255);
    update_leds(); 
    LED++;
    delay(1000/fps); 
}

//BPM
void bpm()
{
    // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
    uint8_t BeatsPerMinute = fps/2;
    CRGBPalette16 palette = PartyColors_p;
    uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
    for( int i = 0; i < NUM_LEDS; i++) { //9948
        leds[i] = ColorFromPalette(palette, gHue+(i*2), beat-gHue+(i*10));
    }
    update_leds(); 
    delay(1000/fps); //screw with this one
}

//JUGGLE
void juggle() {
    // eight colored dots, weaving in and out of sync with each other
    fadeToBlackBy( leds, NUM_LEDS, 20);
    byte dothue = 0;
    for( int i = 0; i < 8; i++) {
        leds[beatsin16(i+7,0,NUM_LEDS)] |= CHSV(dothue, 200, 255);
        dothue += 32;
    }
    update_leds(); 
    delay(1000/120);//maybe make this bigger
}

