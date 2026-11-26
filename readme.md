# CYD Based Cart Scale for Food Pantry and Food Rescue organizations

This is a project to create a simple and inexpensive scale for measuring food donations at free food providers, done initially for the Lebanon Ohio Food Pantry, and volunteers with very sore backs. These
organizations have a need to weigh donations and purchases for reporting and record keeping. 

The value here is that instead of loading up a cart or dolly from the truck, bringing it in, 
then unloading each box from the cart to the scale, then back to a cart, you can simply 
load up the cart, wheel it onto this scale, measure the weight all at once (there are buttons
to chose a cart tare or a dolly tare or a traditional tare setting), and wheel it on back
for stocking. 

The CYD is "Cheap Yellow Display", and is an inexpensive ESP32 based development board with built in touch screen that is widely available and well supported by hobbyists such as myself.

This is a work in progress, documentation will be updated once it is matured. The code works now though.

## Hardware

## Display, touchscreen, and compute module:

```
      https://www.amazon.com/dp/B0D93MBWC2
      Hosyond 3.5 320x480 Touch Screen ESP32 Display with WiFi+BT, ST7796U Driver LCD TFT Screen Module for Arduino IoT
      https://www.lcdwiki.com/res/E32R35T/3.5inch_E32R35T_E32N35T_MicroPython_Demo_Instructions.pdf
      https://www.lcdwiki.com/3.5inch_ESP32-32E_Display
      Micropython library pulled from board demo library, and slightly extended by me to include a "big LED number" capability
```

## Strain gauges
```
      https://www.amazon.com/dp/B07B4DNJ2L
      4 x 50kg Load Cell Half Bridge Strain Gauge Weight Sensor + 1x HX711 Module
      Which included the HX711 sensor
      https://github.com/SergeyPiskunov/micropython-hx711/tree/master
```

## Other Info

I used 3d printed strain gauge holders from Thingiverse scaled up by 1%

Screwed into big rigid board
```
              G1     G3
              G2     G4
```

I modelled a 3d case, but Claude did a better one.  I will post it on thingiverse when it is sorted, email me if you want it before then.  

Another nice thing about this board was that it has very detailed dimensional drawings: https://www.lcdwiki.com/res/E32R35T/E32R35T_Size.pdf

This meant Claude was able to consume these directly and did a nifty job of designing an enclosure.

## Wiring things up (CYD = Cheap Yellow Display ESP32 board I2C)

For connectors between the scale and the CYD, I used some RJ45 sockets with header pins on both ends, so that I can simply use (or crimp new) ethernet 
cables for the connection.  I actually used this a LOONNNG time ago for some other projects, and my Miller TIG welder foot pedal uses this approach.

It is not the cheapest approach, it adds $4 per cart for the two needed connectors, plus the cost of the ethernet cable.  But it is a huge time saver over 
fussing with other ribbon cable options, they are twisted pair so fairly noise resistant, and they are field replaceble at 2am after somebody drives
a cart over it and cuts a conductor.  It also leaves another 4 pins available for future projects.  I keep a pile of them in a drawer.

I used these, and that is what the case is modeled for: https://www.amazon.com/dp/B0B2P9C3DK?th=1

My hookup is therefore as follows.

```

        CYD                RJ-45 Socket     HX711
    =======================================================
        3.3V (Red)              1         VCC (Red)
        SDA/IO32 (Black)        2         Data (Orange)
        SCL/IO25 (Yel)          3         Clk (White)
        Gnd (Grn)               4         Gnd (Black)
```

Wiring things up (HX711 to 4x half bridge strain gauges)
```

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
```


## Setting up the CYD

To set up my CYD board with the micropython environment:

- Windows CMD
- pip install esptool
- python -m esptool to run it
- Download the bin file from  MicroPython - Python for microcontrollers
- python -m esptool --port COM4 --baud 961200 write_flash 0x1000 ESP32_GENERIC-20260824-v1.29.0.bin 
- (Device manager to find com port, and I used cygwin bash, but git bash and windows cmd would probably work fine)
- Then it showed up automatically when I restarted visual studio

I had to set up a Visual Code extension (micropico).  Thonny was nice also, but I spend a lot of time in Visual Studio Code,
and it is pretty impressive.

In a new visual studio code folder, ctrl-+shift+P, the type micropico, then select initialize MicroPico project.
