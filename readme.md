# CYD Based Cart Scale for food pantrys
This is a project to create a simple and inexpensive scale for measuring food donations at free food providers.  

CYD is "Cheap Yellow Display", and is an inexpensive ESP32 based development board with built in touch screen that is widely available and well supported by hobbyists such as myself.

This is a work in progress, documentation will be updated once it is matured. The code works now though.

## Hardware

## Display, touchscreen, and compute module:
      https://www.amazon.com/dp/B0D93MBWC2
      Hosyond 3.5'' 320x480 Touch Screen ESP32 Display with WiFi+BT, ST7796U Driver LCD TFT Screen Module for Arduino IoT
      https://www.lcdwiki.com/res/E32R35T/3.5inch_E32R35T_E32N35T_MicroPython_Demo_Instructions.pdf
      https://www.lcdwiki.com/3.5inch_ESP32-32E_Display
      Micropython library pulled from board demo library, and slightly extended by me to include a "big LED number" capability

##Strain gauges
      https://www.amazon.com/dp/B07B4DNJ2L
      4 x 50kg Load Cell Half Bridge Strain Gauge Weight Sensor + 1x HX711 Module
      Which included the HX711 sensor
      https://github.com/SergeyPiskunov/micropython-hx711/tree/master

3d printed strain gauge holders from Thingiverse module scaled up by 1%
Screwed into big rigid board, see wiring below to HX711
              G1     G3
              G2     G4

Wiring things up (CYD = Cheap Yellow Display ESP32 board I2C)

        CYD                  Ribbon       HX711
    =================================================
        3.3V (Red)           Red          VCC (Red)
        SDA/IO32 (Black)     Orange       Data (Orange)
        SCL/IO25 (Yel)       Yellow       Clk (White)
        Gnd (Grn)            Grn          Gnd (Black)
       
Wiring things up (HX711 to 4x half bridge strain gauges)

    Hx711       Strain Gauge      Strain Gauge
   ============================================
     E-           G1-Red
     A+           G2-Red
     A-           G3-Red
     E+           G4-Red
                  G1-Black          G3-BLack
                  G3-White          G4-White
                  G4-Black          G2-Black
                  G1 White          G2-White